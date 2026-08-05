def calculate_bmi(weight, height):
    """
    Calculate BMI.

    weight = kilograms
    height = meters
    """

    if height <= 0:
        return 0

    bmi = weight / (height ** 2)

    return round(bmi, 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"