"""
Home Page View for HealthGuardian AI
Renders Enterprise SaaS Corporate Healthcare Landing Hero, System Metrics, and Feature Modules.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_home_page():
    """Render Healthcare SaaS Corporate Landing Page."""

    # 1. Enterprise SaaS Hero Banner
    st.markdown("""
    <div class="hero-box animate-fade-in">
        <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div style="flex: 1; min-width: 320px;">
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); padding: 6px 16px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.8px; margin-bottom: 20px; text-transform: uppercase;">
                    <span style="width: 8px; height: 8px; background-color: #38bdf8; border-radius: 50%; display: inline-block;"></span>
                    Clinical Risk Intelligence Platform
                </div>
                <h1 class="hero-title-large">
                    The Bridge for Intelligent Lifestyle Health Care
                </h1>
                <p class="hero-subtitle-large">
                    HealthGuardian AI is a groundbreaking medical decision platform run by AI Engineers and Physicians, delivering real-time risk prediction for Diabetes, Heart Disease, Hypertension, Obesity, Kidney, and Stroke.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Key Performance Metrics Counter Bar
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="glass-card text-center" style="border-top: 3px solid #38bdf8 !important;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8; letter-spacing: -0.5px;">94.5%</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; font-weight: 600; margin-top: 4px;">ROC-AUC Benchmark</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">XGBoost / CatBoost Ensemble</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card text-center" style="border-top: 3px solid #34d399 !important;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #34d399; letter-spacing: -0.5px;">6 Pathology</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; font-weight: 600; margin-top: 4px;">Disease Models</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">Multi-Disease Scoring</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card text-center" style="border-top: 3px solid #fbbf24 !important;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #fbbf24; letter-spacing: -0.5px;">12 Classifiers</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; font-weight: 600; margin-top: 4px;">Auto ML Comparator</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">Scikit-learn & Ensembles</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="glass-card text-center" style="border-top: 3px solid #c084fc !important;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #c084fc; letter-spacing: -0.5px;">SHAP & LIME</div>
            <div style="font-size: 0.88rem; color: #cbd5e1; font-weight: 600; margin-top: 4px;">Explainable AI</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">Feature Attribution Engine</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Enterprise SaaS Modules
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h3 style="font-size: 1.4rem; color: #ffffff;">Enterprise Clinical Capabilities</h3>
        <p style="font-size: 0.9rem; color: #94a3b8;">End-to-end diagnostic risk evaluation and health management infrastructure.</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 1.8rem; margin-bottom: 12px; color: #38bdf8;">🩸</div>
            <h4 style="font-size: 1.15rem; color: #ffffff; margin-bottom: 8px;">Multi-Disease Diagnostics</h4>
            <p style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6;">
                Real-time, independent ML risk estimation for Diabetes, Heart Disease, Hypertension, Obesity, Kidney Disease, and Stroke.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 1.8rem; margin-bottom: 12px; color: #38bdf8;">🧮</div>
            <h4 style="font-size: 1.15rem; color: #ffffff; margin-bottom: 8px;">10 Health Calculators</h4>
            <p style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6;">
                Clinical metrics computation: BMI, Body Fat %, BMR, TDEE, Calorie/Protein target, Water Intake, IBW, WHR, and BSA.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 1.8rem; margin-bottom: 12px; color: #38bdf8;">📑</div>
            <h4 style="font-size: 1.15rem; color: #ffffff; margin-bottom: 8px;">ReportLab Diagnostic PDF</h4>
            <p style="font-size: 0.88rem; color: #94a3b8; line-height: 1.6;">
                Automated clinical report generation complete with QR code verification, risk matrix, AI recommendations, and medical disclaimer.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Quick Action SaaS Shortcuts
    st.markdown("### 🚀 Launch Platform Modules")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)

    with q_col1:
        if st.button("🩸 Run Disease Prediction", use_container_width=True):
            st.session_state.page = "Disease Prediction"
            st.rerun()

    with q_col2:
        if st.button("🧮 Open Health Calculators", use_container_width=True):
            st.session_state.page = "Health Calculators"
            st.rerun()

    with q_col3:
        if st.button("📊 View Analytics Dashboard", use_container_width=True):
            st.session_state.page = "Analytics Dashboard"
            st.rerun()

    with q_col4:
        if st.button("👤 Patient Medical Profile", use_container_width=True):
            st.session_state.page = "Patient Profile"
            st.rerun()
