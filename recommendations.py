def get_diet_recommendation(bmi, risk):

    recommendations = []

    # Underweight
    if bmi < 18.5:

        recommendations.extend([
            "🥛 Drink milk daily",
            "🍌 Eat bananas",
            "🥚 Eat eggs",
            "🥜 Include nuts",
            "🍚 Eat healthy carbohydrates"
        ])

    # Normal
    elif bmi < 25:

        recommendations.extend([
            "🥗 Eat plenty of vegetables",
            "🍎 Eat fresh fruits",
            "🥩 Include lean protein",
            "🥜 Eat healthy nuts",
            "💧 Drink enough water"
        ])

    # Overweight
    elif bmi < 30:

        recommendations.extend([
            "🥦 Eat green vegetables",
            "🍗 Choose grilled chicken or fish",
            "🥣 Eat oats",
            "🚫 Reduce sugar",
            "🚫 Avoid fried food"
        ])

    # Obese
    else:

        recommendations.extend([
            "🥗 High-fiber diet",
            "🍵 Green tea",
            "🥒 Eat cucumber",
            "🥬 Leafy vegetables",
            "🚫 Avoid soft drinks"
        ])

    # High diabetes risk
    if risk >= 60:

        recommendations.extend([
            "🍞 Use whole grains",
            "🥜 Eat almonds",
            "🍓 Eat berries",
            "🚫 Avoid sweets",
            "🚫 Avoid sugary drinks"
        ])

    return recommendations