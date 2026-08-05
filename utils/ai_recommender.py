"""
Rule-Based AI Recommendation Engine for HealthGuardian AI
Generates personalized Diet, Exercise, Hydration, Sleep, and Stress management plans.
"""

from typing import Dict, Any, List
from utils.calculators import calculate_bmi, calculate_water_intake


def generate_ai_recommendations(patient_data: Dict[str, Any], disease_risks: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate tailored medical & lifestyle advice based on clinical rules.
    """
    bmi = patient_data.get("bmi", 24.5)
    glucose = patient_data.get("glucose", 100.0)
    sys_bp = patient_data.get("blood_pressure", 120.0)
    stress = patient_data.get("stress_level", "Moderate")
    sleep = patient_data.get("sleep_hours", 7.5)
    smoking = patient_data.get("smoking", "Never")
    alcohol = patient_data.get("alcohol", "Never")

    dia_risk = disease_risks.get("Diabetes", {}).get("probability", 15.0)
    heart_risk = disease_risks.get("Heart Disease", {}).get("probability", 15.0)
    hyp_risk = disease_risks.get("Hypertension", {}).get("probability", 15.0)

    # 1. Diet Recommendations
    diet_plan = []
    if dia_risk > 40 or glucose > 110:
        diet_plan.append("🥗 Low Glycemic Index (GI) Diet: Focus on complex carbs (oats, quinoa, brown rice) and eliminate refined sugars.")
        diet_plan.append("🥦 High Fiber Intake: Consume 30-35g daily of leafy greens, legumes, and chia seeds to stabilize blood glucose.")
    else:
        diet_plan.append("🥗 Balanced Mediterranean Diet: Lean proteins, healthy fats (olive oil, avocados), and whole grains.")

    if hyp_risk > 40 or sys_bp > 130:
        diet_plan.append("🧂 DASH Diet Sodium Restriction: Limit sodium to under 2,000 mg/day (less than 1 teaspoon of salt).")

    if bmi > 25:
        diet_plan.append("📉 Caloric Deficit: Aim for a moderate 300-500 kcal daily deficit for sustainable 0.5kg/week weight reduction.")
    
    diet_plan.append("🥑 Healthy Fats: Swap saturated fats with Omega-3 rich walnuts, flaxseeds, and fatty fish.")

    # 2. Exercise Recommendations
    exercise_plan = []
    if heart_risk > 50 or sys_bp > 140:
        exercise_plan.append("🏃‍♂️ Moderate Aerobic Exercise: 30 minutes of brisk walking or swimming 5 days/week (keep HR under 70% max).")
        exercise_plan.append("🧘 Low-impact Yoga & Stretching: Enhances vascular elasticity without sudden BP spikes.")
    else:
        exercise_plan.append("🏋️ Hybrid Training: 150 minutes/week moderate aerobic exercise + 2 sessions of progressive resistance training.")
    
    if bmi > 28:
        exercise_plan.append("🚴 Low-Impact Cardio: Cycling, elliptical, or aqua aerobics to protect knee joints.")

    # 3. Hydration Recommendations
    water_liters, glasses_desc = calculate_water_intake(patient_data.get("weight", 70.0), patient_data.get("exercise_freq", "3-4 days/week"))
    hydration_plan = [
        f"💧 Target Daily Intake: {water_liters} Liters ({glasses_desc}).",
        "⏰ Hydration Routine: Drink 1 glass (250ml) immediately upon waking and before each meal.",
        "🚫 Limit Beverage Toxins: Avoid sugary sodas, energy drinks, and excessive caffeine (>2 cups coffee/day)."
    ]

    # 4. Sleep Hygiene Recommendations
    sleep_plan = []
    if sleep < 7.0:
        sleep_plan.append("😴 Target 7.5 - 8.5 Hours of Sleep: Chronic sleep deprivation increases cortisol and insulin resistance.")
        sleep_plan.append("📵 Digital Detox: Avoid blue light screens 60 minutes before bedtime.")
    else:
        sleep_plan.append("😴 Maintain Consistent Sleep/Wake Time: Supports circadian rhythm and metabolic homeostasis.")
    sleep_plan.append("🌡️ Sleep Environment: Maintain a cool (18-20°C), pitch-dark room.")

    # 5. Stress Management
    stress_plan = []
    if stress.lower() in ["high", "severe"]:
        stress_plan.append("🧘 Daily Mindfulness Meditation: 15 minutes of box breathing (4s in, 4s hold, 4s out, 4s hold).")
        stress_plan.append("🌲 Nature Exposure: 20 minutes daily outdoor walking reduces salivary cortisol level by up to 25%.")
    else:
        stress_plan.append("🧘 Active Relaxation: Incorporate deep breathing exercises during work breaks.")

    # 6. Specific Lifestyle Modification Warnings
    lifestyle_warnings = []
    if smoking.lower() != "never":
        lifestyle_warnings.append("⚠️ Smoking Cessation Priority: Smoking doubles cardiovascular risk and damages arterial endothelium.")
    if alcohol.lower() == "regularly":
        lifestyle_warnings.append("⚠️ Alcohol Reduction: Limit intake to zero or strictly under 2 standard units/week.")

    return {
        "diet_plan": diet_plan,
        "exercise_plan": exercise_plan,
        "hydration_plan": hydration_plan,
        "sleep_plan": sleep_plan,
        "stress_plan": stress_plan,
        "lifestyle_warnings": lifestyle_warnings
    }
