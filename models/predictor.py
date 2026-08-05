"""
Independent Disease Risk Predictor for HealthGuardian AI
Provides risk scoring for 6 lifestyle diseases: Diabetes, Heart Disease, Hypertension,
Obesity, Kidney Disease, and Stroke.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.multi_model_trainer import load_model_artifacts
from models.pipeline import preprocess_data, engineer_features


def predict_diabetes_ml(input_features: Dict[str, Any]) -> Tuple[float, str, Any, Any, List[str]]:
    """
    Predict Diabetes Risk using best trained ML model.
    """
    artifacts = load_model_artifacts()
    best_model = artifacts["best_model"]
    scaler = artifacts["scaler"]
    feature_names = artifacts["feature_names"]

    # Construct single sample dataframe
    df_sample = pd.DataFrame([{
        "Pregnancies": input_features.get("pregnancies", 0),
        "Glucose": input_features.get("glucose", 120.0),
        "BloodPressure": input_features.get("blood_pressure", 70.0),
        "SkinThickness": input_features.get("skin_thickness", 20.0),
        "Insulin": input_features.get("insulin", 79.0),
        "BMI": input_features.get("bmi", 25.0),
        "DiabetesPedigreeFunction": input_features.get("dpf", 0.47),
        "Age": input_features.get("age", 35)
    }])

    # Clean & Engineer
    df_clean = preprocess_data(df_sample)
    df_fe = engineer_features(df_clean)

    # Ensure all features exist
    for col in feature_names:
        if col not in df_fe.columns:
            df_fe[col] = 0.0

    X_sample = df_fe[feature_names].values
    X_scaled = scaler.transform(X_sample)

    if hasattr(best_model, "predict_proba"):
        prob = float(best_model.predict_proba(X_scaled)[0, 1])
    else:
        prob = float(best_model.predict(X_scaled)[0])

    prob_pct = round(prob * 100, 1)

    if prob_pct < 25:
        category = "Low Risk"
    elif prob_pct < 55:
        category = "Moderate Risk"
    elif prob_pct < 80:
        category = "High Risk"
    else:
        category = "Severe Risk"

    return prob_pct, category, best_model, X_scaled, feature_names


def predict_heart_disease_risk(age: int, gender: str, sys_bp: float, bmi: float, smoking: str, glucose: float, stress: str) -> Tuple[float, str]:
    """Clinical ASCVD-aligned Heart Disease Risk calculation algorithm."""
    risk_score = 0.0

    # Age impact
    if age > 65:
        risk_score += 25
    elif age > 50:
        risk_score += 18
    elif age > 40:
        risk_score += 10
    else:
        risk_score += 4

    # Gender baseline (Male slightly higher cardiovascular baseline)
    if gender.lower() == "male":
        risk_score += 5

    # Systolic Blood Pressure
    if sys_bp >= 140:
        risk_score += 22
    elif sys_bp >= 130:
        risk_score += 14
    elif sys_bp >= 120:
        risk_score += 8

    # BMI impact
    if bmi >= 35:
        risk_score += 18
    elif bmi >= 30:
        risk_score += 12
    elif bmi >= 25:
        risk_score += 6

    # Smoking status
    if smoking.lower() == "regularly":
        risk_score += 20
    elif smoking.lower() == "occasionally":
        risk_score += 10

    # Glucose level (Diabetic threshold > 125)
    if glucose >= 140:
        risk_score += 15
    elif glucose >= 100:
        risk_score += 8

    # Stress impact
    if stress.lower() == "high":
        risk_score += 10
    elif stress.lower() == "moderate":
        risk_score += 5

    prob = min(98.0, max(3.0, risk_score))
    category = "Low Risk" if prob < 25 else ("Moderate Risk" if prob < 55 else ("High Risk" if prob < 75 else "Severe Risk"))
    return round(prob, 1), category


def predict_hypertension_risk(sys_bp: float, bmi: float, age: int, salt_intake: str = "Moderate", stress: str = "Moderate", exercise: str = "3-4 days/week") -> Tuple[float, str]:
    """Hypertension Risk evaluation model based on JNC-7 guidelines."""
    base_risk = 0.0

    if sys_bp >= 140:
        base_risk += 45
    elif sys_bp >= 130:
        base_risk += 30
    elif sys_bp >= 120:
        base_risk += 18
    else:
        base_risk += 5

    if bmi >= 30:
        base_risk += 20
    elif bmi >= 25:
        base_risk += 10

    if age >= 55:
        base_risk += 15
    elif age >= 40:
        base_risk += 8

    if stress.lower() == "high":
        base_risk += 10

    if exercise.lower() in ["never", "rarely"]:
        base_risk += 10

    prob = min(99.0, max(4.0, base_risk))
    category = "Low Risk" if prob < 25 else ("Moderate Risk" if prob < 55 else ("High Risk" if prob < 75 else "Severe Risk"))
    return round(prob, 1), category


def predict_obesity_risk(bmi: float, exercise: str, sleep_hours: float, stress: str) -> Tuple[float, str]:
    """Obesity Risk classification model based on WHO standards."""
    if bmi >= 35.0:
        prob = 95.0
        category = "Severe Risk"
    elif bmi >= 30.0:
        prob = 80.0
        category = "High Risk"
    elif bmi >= 25.0:
        prob = 50.0
        category = "Moderate Risk"
    else:
        # Check lifestyle risks
        risk = 12.0
        if exercise.lower() in ["never", "rarely"]:
            risk += 15
        if sleep_hours < 6.0:
            risk += 10
        if stress.lower() == "high":
            risk += 8
        prob = min(40.0, risk)
        category = "Low Risk"

    return round(prob, 1), category


def predict_kidney_disease_risk(age: int, sys_bp: float, glucose: float, bmi: float) -> Tuple[float, str]:
    """Chronic Kidney Disease (CKD) risk screening model."""
    risk = 5.0
    if glucose >= 140:
        risk += 30
    elif glucose >= 100:
        risk += 12

    if sys_bp >= 140:
        risk += 28
    elif sys_bp >= 130:
        risk += 14

    if age >= 60:
        risk += 20
    elif age >= 45:
        risk += 10

    if bmi >= 30:
        risk += 10

    prob = min(95.0, max(3.0, risk))
    category = "Low Risk" if prob < 25 else ("Moderate Risk" if prob < 55 else ("High Risk" if prob < 75 else "Severe Risk"))
    return round(prob, 1), category


def predict_stroke_risk(age: int, sys_bp: float, diabetes_prob: float, smoking: str, heart_prob: float) -> Tuple[float, str]:
    """Stroke Risk estimation using Framingham Stroke Study principles."""
    risk = 3.0
    if age > 65:
        risk += 25
    elif age > 50:
        risk += 15

    if sys_bp >= 140:
        risk += 30
    elif sys_bp >= 130:
        risk += 15

    if smoking.lower() == "regularly":
        risk += 18

    if diabetes_prob > 50:
        risk += 15

    if heart_prob > 50:
        risk += 15

    prob = min(96.0, max(2.0, risk))
    category = "Low Risk" if prob < 20 else ("Moderate Risk" if prob < 50 else ("High Risk" if prob < 75 else "Severe Risk"))
    return round(prob, 1), category


def evaluate_all_disease_risks(patient_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Master function evaluating all 6 lifestyle disease risk models.
    """
    # 1. Diabetes ML
    dia_prob, dia_cat, model, X_scaled, feat_names = predict_diabetes_ml(patient_inputs)

    # Patient params extraction
    age = patient_inputs.get("age", 35)
    gender = patient_inputs.get("gender", "Male")
    sys_bp = patient_inputs.get("blood_pressure", 120.0)
    bmi = patient_inputs.get("bmi", 24.5)
    smoking = patient_inputs.get("smoking", "Never")
    glucose = patient_inputs.get("glucose", 100.0)
    stress = patient_inputs.get("stress_level", "Moderate")
    exercise = patient_inputs.get("exercise_freq", "3-4 days/week")
    sleep = patient_inputs.get("sleep_hours", 7.5)

    # 2. Heart Disease
    heart_prob, heart_cat = predict_heart_disease_risk(age, gender, sys_bp, bmi, smoking, glucose, stress)

    # 3. Hypertension
    hyp_prob, hyp_cat = predict_hypertension_risk(sys_bp, bmi, age, stress=stress, exercise=exercise)

    # 4. Obesity Risk
    obe_prob, obe_cat = predict_obesity_risk(bmi, exercise, sleep, stress)

    # 5. Kidney Disease Risk
    kid_prob, kid_cat = predict_kidney_disease_risk(age, sys_bp, glucose, bmi)

    # 6. Stroke Risk
    str_prob, str_cat = predict_stroke_risk(age, sys_bp, dia_prob, smoking, heart_prob)

    return {
        "Diabetes": {"probability": dia_prob, "category": dia_cat},
        "Heart Disease": {"probability": heart_prob, "category": heart_cat},
        "Hypertension": {"probability": hyp_prob, "category": hyp_cat},
        "Obesity": {"probability": obe_prob, "category": obe_cat},
        "Kidney Disease": {"probability": kid_prob, "category": kid_cat},
        "Stroke": {"probability": str_prob, "category": str_cat},
        "best_model": model,
        "X_scaled": X_scaled,
        "feature_names": feat_names
    }
