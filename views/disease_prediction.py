"""
Disease Risk Prediction & Explainable AI View for HealthGuardian AI
Runs 6 independent lifestyle disease risk models, calculates Health Score,
renders SHAP/LIME explainability plots, displays multi-model benchmarks, and exports PDF.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from database.db_handler import save_prediction, get_patient_profile
from models.predictor import evaluate_all_disease_risks
from models.explainability import generate_shap_explanation, generate_lime_explanation
from models.multi_model_trainer import load_model_artifacts
from utils.calculators import calculate_bmi
from utils.health_score import calculate_health_score, create_health_score_gauge
from utils.ai_recommender import generate_ai_recommendations
from reports.pdf_generator import generate_pdf_report


def render_disease_prediction_page():
    """Render Disease Risk Prediction Dashboard & AI Engine."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #1a365d; font-weight: 800;">🩸 Multi-Disease Risk Prediction & Explainable AI</h2>
        <p style="color: #4a5568;">Comprehensive ML risk evaluation for Diabetes, Heart Disease, Hypertension, Obesity, Kidney, and Stroke.</p>
    </div>
    """, unsafe_allow_html=True)

    # Pre-fill from active user session profile if available
    profile = {}
    user = st.session_state.get("user")
    if user:
        profile = get_patient_profile(user["id"])

    with st.form("prediction_input_form"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Patient Physiological & Lifestyle Parameters")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            patient_name = st.text_input("Patient Full Name", value=user.get("full_name", "John Doe") if user else "John Doe")
            age = st.number_input("Age (Years)", 1, 120, int(profile.get("age", 35)))
            gender = st.selectbox("Gender", ["Male", "Female"], index=0 if profile.get("gender") == "Male" else 1)
            pregnancies = st.number_input("Pregnancies", 0, 20, 0 if gender == "Male" else 1)

        with col2:
            glucose = st.number_input("Fasting Glucose (mg/dL)", 40.0, 300.0, 115.0, help="Normal < 100, Pre-diabetes 100-125, Diabetes >= 126")
            blood_pressure = st.number_input("Systolic BP (mmHg)", 60.0, 240.0, 122.0, help="Normal < 120, High >= 130")
            skin_thickness = st.number_input("Triceps Skin Thickness (mm)", 0.0, 99.0, 23.0)
            insulin = st.number_input("2-Hour Serum Insulin (mu U/ml)", 0.0, 840.0, 85.0)

        with col3:
            height = st.number_input("Height (cm)", 50.0, 250.0, float(profile.get("height", 172.0)))
            weight = st.number_input("Weight (kg)", 20.0, 250.0, float(profile.get("weight", 74.0)))
            dpf = st.number_input("Diabetes Pedigree Function", 0.05, 2.50, 0.47, help="Genetic family history indicator")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], index=6)

        with col4:
            smoking = st.selectbox("Smoking Status", ["Never", "Occasionally", "Regularly"], index=["Never", "Occasionally", "Regularly"].index(profile.get("smoking", "Never")))
            alcohol = st.selectbox("Alcohol Intake", ["Never", "Occasionally", "Regularly"], index=["Never", "Occasionally", "Regularly"].index(profile.get("alcohol", "Never")))
            sleep_hours = st.slider("Sleep (Hours/Night)", 3.0, 12.0, float(profile.get("sleep_hours", 7.5)), 0.5)
            stress_level = st.select_slider("Stress Level", ["Low", "Moderate", "High"], value=profile.get("stress_level", "Moderate"))
            exercise_freq = st.selectbox("Exercise Frequency", ["Never / Sedentary", "1-2 days/week", "3-4 days/week", "5+ days/week (Active)"], index=2)

        bmi, bmi_cat, _ = calculate_bmi(weight, height)
        st.info(f"💡 Calculated Body Mass Index (BMI): **{bmi} kg/m²** ({bmi_cat})")
        st.markdown('</div>', unsafe_allow_html=True)

        btn_submit = st.form_submit_button("⚡ Run Full AI Risk Diagnosis", use_container_width=True)

    if btn_submit:
        patient_inputs = {
            "pregnancies": pregnancies,
            "glucose": glucose,
            "blood_pressure": blood_pressure,
            "skin_thickness": skin_thickness,
            "insulin": insulin,
            "bmi": bmi,
            "dpf": dpf,
            "age": age,
            "gender": gender,
            "smoking": smoking,
            "alcohol": alcohol,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "exercise_freq": exercise_freq,
            "height": height,
            "weight": weight,
            "blood_group": blood_group
        }

        with st.spinner("Processing ML multi-disease risk evaluation ensembled pipeline..."):
            # 1. Run disease risks evaluation
            disease_risks = evaluate_all_disease_risks(patient_inputs)

            # 2. Calculate Health Score
            health_score, health_status, score_color = calculate_health_score(patient_inputs, disease_risks)

            # 3. Generate AI recommendations
            ai_recs = generate_ai_recommendations(patient_inputs, disease_risks)

            # 4. Save to database if user logged in
            if user:
                save_prediction(
                    user_id=user["id"],
                    age=age,
                    bmi=bmi,
                    glucose=glucose,
                    blood_pressure=blood_pressure,
                    diabetes_prob=disease_risks["Diabetes"]["probability"],
                    heart_prob=disease_risks["Heart Disease"]["probability"],
                    hypertension_prob=disease_risks["Hypertension"]["probability"],
                    obesity_prob=disease_risks["Obesity"]["probability"],
                    kidney_prob=disease_risks["Kidney Disease"]["probability"],
                    stroke_prob=disease_risks["Stroke"]["probability"],
                    health_score=health_score,
                    details={
                        "patient_name": patient_name,
                        "risks": {k: v for k, v in disease_risks.items() if k not in ["best_model", "X_scaled", "feature_names"]},
                        "recommendations": ai_recs
                    }
                )

        st.success("Diagnostic Evaluation Completed Successfully!")

        # --- RESULTS DISPLAY ---
        st.markdown("### 📊 Diagnostic Results Overview")

        r_col1, r_col2 = st.columns([1, 1])

        # Column 1: Health Score Gauge Chart
        with r_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            gauge_fig = create_health_score_gauge(health_score, health_status, score_color)
            st.plotly_chart(gauge_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Column 2: Disease Risk Breakdown Cards
        with r_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### Lifestyle Disease Risk Scores")

            for disease_name, risk_info in disease_risks.items():
                if isinstance(risk_info, dict) and "probability" in risk_info:
                    prob = risk_info["probability"]
                    cat = risk_info["category"]

                    if prob < 25:
                        badge_class = "badge-low"
                        bar_color = "#38a169"
                    elif prob < 55:
                        badge_class = "badge-moderate"
                        bar_color = "#3182ce"
                    else:
                        badge_class = "badge-high"
                        bar_color = "#e53e3e"

                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 4px;">
                            <span>{disease_name}</span>
                            <span>{prob}% <span class="{badge_class}">{cat}</span></span>
                        </div>
                        <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: {bar_color}; width: {prob}%; height: 100%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # --- EXPLAINABLE AI (SHAP & LIME) ---
        st.markdown("---")
        st.markdown("### 🧠 Explainable AI (XAI) Insights")

        xai_col1, xai_col2 = st.columns(2)

        best_model = disease_risks["best_model"]
        X_scaled = disease_risks["X_scaled"]
        feat_names = disease_risks["feature_names"]
        artifacts = load_model_artifacts()
        X_train = artifacts.get("X_train", X_scaled)

        with xai_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### SHAP Feature Impact")
            shap_res = generate_shap_explanation(best_model, X_train, X_scaled, feat_names)
            st.pyplot(shap_res["figure"])
            st.markdown('</div>', unsafe_allow_html=True)

        with xai_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### LIME Local Feature Weight")
            lime_res = generate_lime_explanation(best_model, X_train, X_scaled, feat_names)
            st.pyplot(lime_res["figure"])
            st.markdown('</div>', unsafe_allow_html=True)

        # --- MODEL COMPARISON BENCHMARK TABLE ---
        st.markdown("---")
        st.markdown("### 🤖 ML Multi-Model Benchmark & Comparison")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        results_df = artifacts["results_df"]
        st.dataframe(
            results_df[["Model", "Accuracy", "CV Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]],
            use_container_width=True
        )
        st.caption(f"🏆 Automatically Selected Best Model: **{artifacts['best_model_name']}** based on test validation accuracy.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- AI RECOMMENDATIONS & PDF DOWNLOAD ---
        st.markdown("---")
        st.markdown("### 📋 AI Personal Action Plan & Report Export")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🥗 Diet Plan", "🏃 Exercise Plan", "💧 Lifestyle & Hydration"])

        with t1:
            for item in ai_recs["diet_plan"]:
                st.markdown(f"- {item}")
        with t2:
            for item in ai_recs["exercise_plan"]:
                st.markdown(f"- {item}")
        with t3:
            for item in ai_recs["hydration_plan"] + ai_recs["sleep_plan"] + ai_recs["stress_plan"]:
                st.markdown(f"- {item}")

        st.markdown("<br>", unsafe_allow_html=True)

        pdf_bytes = generate_pdf_report(
            patient_name=patient_name,
            patient_data=patient_inputs,
            disease_risks=disease_risks,
            health_score=health_score,
            health_status=health_status,
            ai_recommendations=ai_recs
        )

        st.download_button(
            label="📄 Download Official PDF Diagnostic Report",
            data=pdf_bytes,
            file_name=f"HealthGuardian_Report_{patient_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
