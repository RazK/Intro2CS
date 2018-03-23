#!python3
#############################################################
# FILE : shapes.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module for helping harry potter calculate
# various shape areas.
#############################################################
import math

SHAPE_CODES = {"circle": 1, "rectangle": 2, "trapezoid": 3}


def shape_area():
    """Prompts the user to choose a shape (1=circle, 2=rectangle, 3=trapezoid),
    and then enter relevant shape parameters:
        circle (1)      - radius
        rectangle(2)    - length, width
        trapezoid(3)    - base1, base2, height
    Returns the area of the desired shape.
    """
    # Parse user input
    shape_code = input_number("Choose shape (1=circle, 2=rectangle, 3=trapezoid): ")

    if (shape_code not in SHAPE_CODES.values()):
        # print("Invalid shape code [{0}].".format(shape_code))
        return None

    elif (shape_code == SHAPE_CODES["circle"]):
        # Parse circle radius
        radius = input_number()
        return circle_area(radius)

    elif (shape_code == SHAPE_CODES["rectangle"]):
        # Parse rectangle length and width
        length = input_number()
        width = input_number()
        return rectangle_area(length, width)

    elif (shape_code == SHAPE_CODES["trapezoid"]):
        # Parse trapezoid bases and height
        base1 = input_number()
        base2 = input_number()
        height = input_number()
        return trapezoid_area(base1, base2, height)

    else:
        # print ("This shape is under development, stay tuned for updates from HUJI!")
        return None


def input_number(message=""):
    """Prompts the user to input according to a message.
    Returns the input converted to a number."""
    return float(input(message).split(' ')[0])


def circle_area(radius):
    """Returns the area of a circle with the given radius."""
    return (math.pi * (radius**2))


def rectangle_area(length, width):
    """Returns the area of a rectangle with the given length and width."""
    return (length * width)


def trapezoid_area(base1, base2, height):
    """Returns the area of a trapzoid with the given bases lengths and
    height."""
    return (height) * (base1 + base2) / 2
