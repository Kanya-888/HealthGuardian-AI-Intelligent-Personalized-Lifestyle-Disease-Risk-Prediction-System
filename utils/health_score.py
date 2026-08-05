"""
Health Score & Gauge Visualization Engine for HealthGuardian AI
Computes a composite Health Index Score (0-100) and renders a Plotly Gauge Chart.
"""

from typing import Dict, Any, Tuple
import plotly.graph_objects as go


def calculate_health_score(patient_data: Dict[str, Any], disease_risks: Dict[str, Any]) -> Tuple[int, str, str]:
    """
    Calculate composite Health Score (0-100).
    Base score: 100
    Applies penalties & bonuses based on clinical thresholds.
    """
    score = 100

    # 1. BMI Penalty
    bmi = patient_data.get("bmi", 24.0)
    if bmi < 18.5 or bmi >= 35:
        score -= 20
    elif bmi >= 30:
        score -= 15
    elif bmi >= 25:
        score -= 8

    # 2. Exercise Bonus / Penalty
    exercise = patient_data.get("exercise_freq", "3-4 days/week").lower()
    if "daily" in exercise or "5" in exercise:
        score += 5
    elif "never" in exercise or "rarely" in exercise:
        score -= 15
    elif "1-2" in exercise:
        score -= 5

    # 3. Sleep Penalty
    sleep = patient_data.get("sleep_hours", 7.5)
    if sleep < 6.0:
        score -= 10
    elif sleep < 7.0:
        score -= 5

    # 4. Stress Penalty
    stress = patient_data.get("stress_level", "Moderate").lower()
    if stress == "high":
        score -= 12
    elif stress == "moderate":
        score -= 4

    # 5. Smoking Penalty
    smoking = patient_data.get("smoking", "Never").lower()
    if smoking == "regularly":
        score -= 20
    elif smoking == "occasionally":
        score -= 10

    # 6. Alcohol Penalty
    alcohol = patient_data.get("alcohol", "Never").lower()
    if alcohol == "regularly":
        score -= 15
    elif alcohol == "occasionally":
        score -= 5

    # 7. Disease Risks Deduction (average risk impact)
    risk_probs = [
        v["probability"] for k, v in disease_risks.items()
        if isinstance(v, dict) and "probability" in v
    ]
    if risk_probs:
        avg_risk = sum(risk_probs) / len(risk_probs)
        risk_penalty = int(avg_risk * 0.35)
        score -= risk_penalty

    # Clamp score between 10 and 100
    final_score = int(max(10, min(100, score)))

    if final_score >= 85:
        status = "Excellent"
        color = "#38a169"
    elif final_score >= 70:
        status = "Good"
        color = "#3182ce"
    elif final_score >= 50:
        status = "Fair / Moderate Risk"
        color = "#dd6b20"
    else:
        status = "Needs Urgent Attention"
        color = "#e53e3e"

    return final_score, status, color


def create_health_score_gauge(score: int, status: str, color: str) -> go.Figure:
    """
    Renders Plotly Gauge Chart for Health Score.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>Health Score Index</b><br><span style='font-size:0.8em;color:{color}'>{status}</span>", 'font': {'size': 20}},
        number={'suffix': "/100", 'font': {'size': 36, 'color': color, 'family': 'Arial'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#4a5568"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#cbd5e0",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(229, 62, 62, 0.25)'},
                {'range': [50, 70], 'color': 'rgba(221, 107, 32, 0.25)'},
                {'range': [70, 85], 'color': 'rgba(49, 130, 206, 0.25)'},
                {'range': [85, 100], 'color': 'rgba(56, 161, 105, 0.25)'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#2d3748", 'family': "Arial"},
        height=320,
        margin=dict(l=30, r=30, t=50, b=30)
    )

    return fig
