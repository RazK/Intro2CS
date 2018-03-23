#!python3
#############################################################
# FILE : bmi.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module for helping Hagrid getting in shape.
#############################################################

BMI_THRESHOLD_LOW = 18.5
BMI_THRESHOLD_HIGH = 24.9


def is_normal_bmi(weight, height):
    """Gets a person's weight (kg) and height (meters).
    Returns True if the person is normal weight, False otherwise."""
    bmi = weight / (height**2)
    return (BMI_THRESHOLD_LOW <= bmi and bmi <= BMI_THRESHOLD_HIGH)
