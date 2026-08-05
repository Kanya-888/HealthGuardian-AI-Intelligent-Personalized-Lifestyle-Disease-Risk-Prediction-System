def get_exercise_recommendation(bmi, activity):

    exercises = []

    # Underweight
    if bmi < 18.5:
        exercises.extend([
            "🏋️ Strength Training - 3 days/week",
            "🚶 Walking - 20 minutes/day",
            "🧘 Stretching - 10 minutes/day"
        ])

    # Normal Weight
    elif bmi < 25:
        exercises.extend([
            "🏃 Jogging - 30 minutes/day",
            "🚴 Cycling - 30 minutes/day",
            "🧘 Yoga - 20 minutes/day"
        ])

    # Overweight
    elif bmi < 30:
        exercises.extend([
            "🚶 Brisk Walking - 45 minutes/day",
            "🚴 Cycling - 30 minutes/day",
            "🏊 Swimming - 30 minutes/day"
        ])

    # Obese
    else:
        exercises.extend([
            "🚶 Walking - 60 minutes/day",
            "🧘 Chair Yoga",
            "🏊 Swimming",
            "🚴 Stationary Cycling"
        ])

    # Activity Level Suggestions
    if activity == "Sedentary":
        exercises.append("💡 Start with 20–30 minutes of walking every day.")

    elif activity == "Lightly Active":
        exercises.append("💡 Aim for at least 150 minutes of exercise each week.")

    elif activity == "Moderately Active":
        exercises.append("💡 Maintain your routine and include strength training twice a week.")

    elif activity == "Very Active":
        exercises.append("💡 Include rest and recovery days to avoid overtraining.")

    else:
        exercises.append("💡 Stay hydrated and ensure adequate recovery.")

    return exercises