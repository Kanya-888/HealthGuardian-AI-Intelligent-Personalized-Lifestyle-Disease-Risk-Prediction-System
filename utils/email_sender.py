"""
Email Sender Utility for HealthGuardian AI
Provides SMTP emailing support to dispatch PDF Health Reports directly to patient emails.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Tuple


def send_pdf_report_email(recipient_email: str, patient_name: str, pdf_bytes: bytes,
                         smtp_server: str = "smtp.gmail.com", smtp_port: int = 587,
                         sender_email: str = "", sender_password: str = "") -> Tuple[bool, str]:
    """
    Send generated PDF report as an email attachment.
    """
    if not recipient_email or "@" not in recipient_email:
        return False, "Invalid recipient email address."

    if not sender_email or not sender_password:
        return False, "SMTP sender credentials not configured. Please configure email credentials in Settings."

    try:
        msg = MIMEMultipart()
        msg['From'] = f"HealthGuardian AI <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"Your Personalized Health Guardian Diagnostic Report - {patient_name}"

        body = f"""Dear {patient_name},

Thank you for utilizing HealthGuardian AI – Intelligent Personalized Lifestyle Disease Risk Prediction System.

Please find attached your complete, confidential Medical & Lifestyle Disease Risk Analysis Report in PDF format.

This report includes:
- Composite Health Score Index
- 6 Lifestyle Disease Risk Predictions
- Personalized AI Diet, Exercise, and Hydration Action Plan
- Medical Calculators & Metrics Summary

Wishing you optimal health,

HealthGuardian AI Clinical Analytics Team
"""
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"HealthGuardian_Report_{patient_name.replace(' ', '_')}.pdf")
        msg.attach(pdf_attachment)

        # Send SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return True, f"Report successfully emailed to {recipient_email}!"

    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
