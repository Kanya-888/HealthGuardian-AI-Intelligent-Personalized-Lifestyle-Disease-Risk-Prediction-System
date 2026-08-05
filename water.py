def calculate_water_intake(weight):
    """
    Calculate recommended daily water intake.

    Formula:
    Water (ml) = Weight × 35
    """

    water_ml = weight * 35

    water_liters = water_ml / 1000

    return round(water_ml), round(water_liters, 2)