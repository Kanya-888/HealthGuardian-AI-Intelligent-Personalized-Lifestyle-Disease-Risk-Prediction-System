"""
PDF Report Generator Module for HealthGuardian AI
Generates production-quality medical PDF diagnostic reports using ReportLab.
Includes: Hospital Header, Patient Profile, Health Score, 6 Disease Risk Matrix,
AI Action Plans, QR Code Verification, and Medical Disclaimer.
"""

import io
import os
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.barcode import qr


def generate_pdf_report(patient_name: str, patient_data: Dict[str, Any],
                        disease_risks: Dict[str, Any], health_score: int,
                        health_status: str, ai_recommendations: Dict[str, Any]) -> bytes:
    """
    Build a complete, professional Medical PDF Report.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1a365d')
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#4a5568')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=6
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#2d3748')
    )

    bold_text = ParagraphStyle(
        'BoldText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1a202c')
    )

    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#718096')
    )

    # 1. Header Table (Title & QR Code)
    report_date = datetime.now().strftime("%B %d, %Y - %H:%M")
    
    # Generate QR Code Widget
    qr_code = qr.QrCodeWidget(f"HealthGuardian AI Verification ID: HG-{patient_name[:3].upper()}-{datetime.now().strftime('%Y%m%d%H%M')}")
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(60, 60, transform=[60.0/width, 0, 0, 60.0/height, 0, 0])
    d.add(qr_code)

    header_left = [
        Paragraph("<b>HEALTHGUARDIAN AI CLINICAL LABS</b>", title_style),
        Paragraph("Intelligent Lifestyle Disease Risk & Diagnostic Report", subtitle_style),
        Paragraph(f"<b>Report Date:</b> {report_date}", subtitle_style)
    ]

    header_table_data = [[header_left, d]]
    header_table = Table(header_table_data, colWidths=[420, 120])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2b6cb0'), spaceBefore=8, spaceAfter=12))

    # 2. Patient Demographics & Summary Box
    story.append(Paragraph("1. Patient Profile Summary", section_heading))
    
    gender = patient_data.get("gender", "Male")
    age = patient_data.get("age", 35)
    bmi = patient_data.get("bmi", 24.5)
    blood_group = patient_data.get("blood_group", "O+")
    height = patient_data.get("height", 170.0)
    weight = patient_data.get("weight", 70.0)
    bp = patient_data.get("blood_pressure", 120.0)
    glucose = patient_data.get("glucose", 100.0)

    demo_data = [
        [
            Paragraph("<b>Patient Name:</b>", normal_text), Paragraph(patient_name, bold_text),
            Paragraph("<b>Age / Gender:</b>", normal_text), Paragraph(f"{age} Yrs / {gender}", bold_text)
        ],
        [
            Paragraph("<b>Height / Weight:</b>", normal_text), Paragraph(f"{height} cm / {weight} kg", normal_text),
            Paragraph("<b>Blood Group:</b>", normal_text), Paragraph(blood_group, bold_text)
        ],
        [
            Paragraph("<b>BMI:</b>", normal_text), Paragraph(f"{bmi} kg/m²", bold_text),
            Paragraph("<b>Blood Pressure:</b>", normal_text), Paragraph(f"{bp} mmHg", normal_text)
        ],
        [
            Paragraph("<b>Fasting Glucose:</b>", normal_text), Paragraph(f"{glucose} mg/dL", normal_text),
            Paragraph("<b>Smoking / Alcohol:</b>", normal_text), Paragraph(f"{patient_data.get('smoking','Never')} / {patient_data.get('alcohol','Never')}", normal_text)
        ]
    ]

    demo_table = Table(demo_data, colWidths=[110, 160, 110, 160])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 10))

    # 3. Composite Health Score Banner
    story.append(Paragraph("2. Composite Health Index Score", section_heading))
    score_color = colors.HexColor('#38a169') if health_score >= 70 else (colors.HexColor('#dd6b20') if health_score >= 50 else colors.HexColor('#e53e3e'))
    
    score_data = [[
        Paragraph(f"<font size=16 color='white'><b>OVERALL HEALTH SCORE: {health_score} / 100</b></font><br/><font size=11 color='white'>Classification: {health_status}</font>", normal_text)
    ]]
    score_table = Table(score_data, colWidths=[540])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), score_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 12))

    # 4. Lifestyle Disease Risk Assessment Table
    story.append(Paragraph("3. Multi-Disease Risk Prediction Matrix", section_heading))
    
    risk_table_headers = ["Lifestyle Disease", "Risk Probability (%)", "Risk Category", "Clinical Action Standard"]
    table_rows = [[Paragraph(f"<b>{h}</b>", bold_text) for h in risk_table_headers]]

    for disease_name, risk_info in disease_risks.items():
        if isinstance(risk_info, dict) and "probability" in risk_info:
            prob = risk_info["probability"]
            cat = risk_info["category"]
            
            if prob < 25:
                cat_color = "#38a169"
                action = "Routine annual monitoring"
            elif prob < 55:
                cat_color = "#3182ce"
                action = "Lifestyle optimization & dietary change"
            elif prob < 75:
                cat_color = "#dd6b20"
                action = "Clinical consultation & diagnostic testing"
            else:
                cat_color = "#e53e3e"
                action = "Urgent medical evaluation"

            row = [
                Paragraph(f"<b>{disease_name}</b>", normal_text),
                Paragraph(f"{prob}%", bold_text),
                Paragraph(f"<font color='{cat_color}'><b>{cat}</b></font>", normal_text),
                Paragraph(action, normal_text)
            ]
            table_rows.append(row)

    risk_table = Table(table_rows, colWidths=[130, 110, 110, 190])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 12))

    # 5. Personalized AI Action Plan
    story.append(Paragraph("4. Personalized AI Lifestyle Action Plan", section_heading))
    
    plans = [
        ("🥗 Diet & Nutrition Plan", ai_recommendations.get("diet_plan", [])),
        ("🏃 Physical Activity Plan", ai_recommendations.get("exercise_plan", [])),
        ("💧 Hydration & Sleep Hygiene", ai_recommendations.get("hydration_plan", []) + ai_recommendations.get("sleep_plan", []))
    ]

    for plan_title, items in plans:
        story.append(Paragraph(f"<b>{plan_title}</b>", bold_text))
        for item in items:
            clean_item = item.encode('ascii', 'ignore').decode('ascii') if not item.isascii() else item
            story.append(Paragraph(f"• {clean_item}", normal_text))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # 6. Legal & Medical Disclaimer Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e0'), spaceBefore=8, spaceAfter=8))
    disclaimer_text = (
        "<b>MEDICAL DISCLAIMER:</b> HealthGuardian AI predictions are generated using Machine Learning statistical models "
        "and clinical scoring guidelines for informational and educational purposes only. This report does not constitute "
        "medical diagnosis, prescription, or professional treatment advice. Always consult a licensed healthcare professional "
        "or physician regarding any medical conditions or health concerns."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    return buffer.getvalue()
