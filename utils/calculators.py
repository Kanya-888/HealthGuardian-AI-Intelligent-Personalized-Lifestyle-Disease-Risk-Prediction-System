"""
Health Calculators Module for HealthGuardian AI
Implements 10 clinical and physiological calculators:
1. BMI (Body Mass Index)
2. Body Fat Percentage
3. Daily Water Intake
4. Daily Calorie Needs
5. Protein Requirement
6. Ideal Body Weight
7. BMR (Basal Metabolic Rate)
8. TDEE (Total Daily Energy Expenditure)
9. Waist-to-Hip Ratio (WHR)
10. Body Surface Area (BSA)
"""

import math
from typing import Dict, Any, Tuple


def calculate_bmi(weight_kg: float, height_cm: float) -> Tuple[float, str, str]:
    """Calculate BMI, category, and health color code."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "Invalid Input", "#a0aec0"

    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
        color = "#3182ce"
    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
        color = "#38a169"
    elif 25.0 <= bmi < 29.9:
        category = "Overweight"
        color = "#dd6b20"
    elif 30.0 <= bmi < 34.9:
        category = "Obesity Class I"
        color = "#e53e3e"
    elif 35.0 <= bmi < 39.9:
        category = "Obesity Class II"
        color = "#c53030"
    else:
        category = "Severe Obesity (Class III)"
        color = "#9b2c2c"

    return bmi, category, color


def calculate_body_fat(bmi: float, age: int, gender: str) -> Tuple[float, str]:
    """Estimate Body Fat Percentage using Deurenberg formula."""
    gender_factor = 1 if gender.lower() == "male" else 0
    fat_pct = (1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4
    fat_pct = round(max(5.0, min(60.0, fat_pct)), 1)

    if gender.lower() == "male":
        category = "Essential Fat" if fat_pct < 6 else ("Athletic" if fat_pct < 14 else ("Fitness" if fat_pct < 18 else ("Acceptable" if fat_pct < 25 else "High Fat")))
    else:
        category = "Essential Fat" if fat_pct < 14 else ("Athletic" if fat_pct < 21 else ("Fitness" if fat_pct < 25 else ("Acceptable" if fat_pct < 32 else "High Fat")))

    return fat_pct, category


def calculate_water_intake(weight_kg: float, exercise_freq: str = "3-4 days/week") -> Tuple[float, str]:
    """Calculate recommended daily water intake in Liters."""
    base_liters = weight_kg * 0.035  # ~35ml per kg body weight

    if "5" in exercise_freq or "daily" in exercise_freq.lower():
        extra = 0.75
    elif "3" in exercise_freq:
        extra = 0.5
    else:
        extra = 0.25

    total_liters = round(base_liters + extra, 2)
    glasses = int(round(total_liters * 4.0))  # 250ml per glass
    return total_liters, f"{glasses} glasses (250ml each)"


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Calculate BMR using Mifflin-St Jeor Equation."""
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    return round(max(800.0, bmr), 1)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure (TDEE)."""
    multipliers = {
        "Sedentary (Little or no exercise)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (Physical Job / 2x training)": 1.9
    }
    multiplier = multipliers.get(activity_level, 1.375)
    return round(bmr * multiplier, 1)


def calculate_calories_breakdown(tdee: float, goal: str = "Maintain Weight") -> Tuple[float, Dict[str, float]]:
    """Determine daily target calories and macronutrient breakdown."""
    if goal == "Weight Loss (Mild)":
        target = tdee - 300
    elif goal == "Weight Loss (Aggressive)":
        target = tdee - 600
    elif goal == "Weight Gain":
        target = tdee + 400
    else:
        target = tdee

    target = round(max(1200.0, target), 1)

    # Macros: 50% Carbs, 25% Protein, 25% Fat
    carbs_g = round((target * 0.50) / 4.0, 1)
    protein_g = round((target * 0.25) / 4.0, 1)
    fat_g = round((target * 0.25) / 9.0, 1)

    return target, {"Carbs (g)": carbs_g, "Protein (g)": protein_g, "Fat (g)": fat_g}


def calculate_protein_requirement(weight_kg: float, activity_level: str) -> Tuple[float, str]:
    """Calculate target protein requirement in grams per day."""
    if "Very Active" in activity_level or "Extra" in activity_level:
        factor = 1.8
    elif "Moderately" in activity_level:
        factor = 1.4
    else:
        factor = 1.0

    protein_g = round(weight_kg * factor, 1)
    return protein_g, f"{factor}g per kg body weight"


def calculate_ideal_weight(height_cm: float, gender: str) -> Tuple[float, float]:
    """Calculate Ideal Body Weight range using Devine & Robinson Formulas."""
    height_inches = height_cm / 2.54
    over_5ft = max(0.0, height_inches - 60)

    if gender.lower() == "male":
        ibw = 50.0 + (2.3 * over_5ft)
    else:
        ibw = 45.5 + (2.3 * over_5ft)

    ibw = round(ibw, 1)
    min_weight = round(ibw * 0.9, 1)
    max_weight = round(ibw * 1.1, 1)
    return min_weight, max_weight


def calculate_whr(waist_cm: float, hip_cm: float, gender: str) -> Tuple[float, str]:
    """Calculate Waist-to-Hip Ratio (WHR)."""
    if hip_cm <= 0:
        return 0.0, "Invalid Input"

    whr = round(waist_cm / hip_cm, 2)
    if gender.lower() == "male":
        category = "Low Risk" if whr <= 0.90 else ("Moderate Risk" if whr <= 0.99 else "High Risk (Abdominal Obesity)")
    else:
        category = "Low Risk" if whr <= 0.80 else ("Moderate Risk" if whr <= 0.84 else "High Risk (Abdominal Obesity)")

    return whr, category


def calculate_bsa(height_cm: float, weight_kg: float) -> float:
    """Calculate Body Surface Area (BSA) using Mosteller formula."""
    bsa = math.sqrt((height_cm * weight_kg) / 3600.0)
    return round(bsa, 2)
