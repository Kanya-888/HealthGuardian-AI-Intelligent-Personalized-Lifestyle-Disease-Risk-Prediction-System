def calculate_health_score(
    bmi,
    water_liters,
    activity,
    diabetes_risk
):

    score = 100

    # BMI
    if bmi < 18.5:
        score -= 10

    elif bmi >= 30:
        score -= 20

    elif bmi >= 25:
        score -= 10

    # Water Intake
    if water_liters < 2:
        score -= 10

    # Activity
    if activity == "Sedentary":
        score -= 15

    elif activity == "Lightly Active":
        score -= 5

    # Diabetes Risk
    if diabetes_risk > 60:
        score -= 25

    elif diabetes_risk > 30:
        score -= 10

    if score < 0:
        score = 0

    return score