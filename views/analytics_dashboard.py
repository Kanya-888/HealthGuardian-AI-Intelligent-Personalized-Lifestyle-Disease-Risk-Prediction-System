"""
Analytics Dashboard View for HealthGuardian AI
Provides interactive Plotly visualizations: Radar charts, Bar charts, Pie charts, Line charts,
and trend analysis over patient history records.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database.db_handler import get_user_predictions, get_all_predictions


def render_analytics_dashboard_page():
    """Render Interactive Medical Analytics Dashboard."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">📊 Interactive Health Analytics & Risk Trends</h2>
        <p style="color: #4a5568;">Visual exploration of multi-disease risk factors, patient history trends, and population metrics.</p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")

    if user and user.get("role") == "admin":
        history = get_all_predictions()
        st.info("ℹ️ Displaying System-Wide Analytics for Admin")
    elif user:
        history = get_user_predictions(user["id"])
    else:
        history = []

    # If no records exist yet, generate sample data for visual demonstration
    if not history:
        st.warning("No prediction history recorded yet. Below is a demonstration overview.")
        sample_risks = {
            "Diabetes": 45.2,
            "Heart Disease": 28.5,
            "Hypertension": 55.0,
            "Obesity": 62.0,
            "Kidney Disease": 18.0,
            "Stroke": 22.0
        }
    else:
        latest = history[0]
        sample_risks = {
            "Diabetes": latest.get("diabetes_prob", 20.0),
            "Heart Disease": latest.get("heart_prob", 20.0),
            "Hypertension": latest.get("hypertension_prob", 20.0),
            "Obesity": latest.get("obesity_prob", 20.0),
            "Kidney Disease": latest.get("kidney_prob", 20.0),
            "Stroke": latest.get("stroke_prob", 20.0)
        }

    # 1. Row 1: Radar Chart & Risk Bar Chart
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Patient Lifestyle & Disease Radar Profile")

        categories = list(sample_risks.keys())
        values = list(sample_risks.values())

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(49, 130, 206, 0.35)',
            line=dict(color='#2b6cb0', width=2),
            name='Risk Score (%)'
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Disease Risk Distribution")

        df_bar = pd.DataFrame({
            "Disease": list(sample_risks.keys()),
            "Risk (%)": list(sample_risks.values())
        })

        fig_bar = px.bar(
            df_bar,
            x="Disease",
            y="Risk (%)",
            color="Risk (%)",
            color_continuous_scale="Reds" if max(sample_risks.values()) > 50 else "Blues",
            text="Risk (%)"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            xaxis_title="",
            margin=dict(l=20, r=20, t=30, b=30)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Row 2: Health Score Trend Line & Risk Category Pie Chart
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Health Score Progress Trend")

        if len(history) > 1:
            df_hist = pd.DataFrame(history)
            df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'])
            df_hist = df_hist.sort_values(by='timestamp')

            fig_line = px.line(
                df_hist,
                x="timestamp",
                y="health_score",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["#38a169"]
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320,
                xaxis_title="Time of Diagnostic Test",
                yaxis_title="Health Score (0-100)"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            # Sample line trend
            df_sample_line = pd.DataFrame({
                "Test Sequence": ["Session 1", "Session 2", "Session 3", "Current"],
                "Health Score": [62, 68, 74, 82]
            })
            fig_line = px.line(
                df_sample_line,
                x="Test Sequence",
                y="Health Score",
                markers=True,
                color_discrete_sequence=["#3182ce"]
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320
            )
            st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Patient Risk Category Breakdown")

        risk_cats = {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Severe Risk": 0}
        for score in sample_risks.values():
            if score < 25:
                risk_cats["Low Risk"] += 1
            elif score < 55:
                risk_cats["Moderate Risk"] += 1
            elif score < 75:
                risk_cats["High Risk"] += 1
            else:
                risk_cats["Severe Risk"] += 1

        fig_pie = px.pie(
            names=list(risk_cats.keys()),
            values=list(risk_cats.values()),
            hole=0.4,
            color=list(risk_cats.keys()),
            color_discrete_map={
                "Low Risk": "#38a169",
                "Moderate Risk": "#3182ce",
                "High Risk": "#dd6b20",
                "Severe Risk": "#e53e3e"
            }
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
