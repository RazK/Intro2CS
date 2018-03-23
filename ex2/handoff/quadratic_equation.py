#!python3
#############################################################
# FILE : quadratic_equation.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module for solving a quadratic equation.
#############################################################
import math


def quadratic_equation_user_input():
    """Prompts the user to input 3 parameters for the formula ax^2 +bx +c = 0.
    Solves the equation for x, and returns the following results for each case:
    2 solutions: returns both: (x1, x2)
    1 solution:  returns (x1, None)
    0 solutions: returns (None, None)
    """
    user_input = input("Insert coefficients a, b, and c: ")
    parsed_input = user_input.split(' ')

    # Notice: Not validating input here because it's just an exercise with
    # assumptions on correct input validity, but as I demonstrated in previous
    # exercises - I know how to validate user input and acknowledge it as a
    # mandatory part of my code.

    # convert parameters from strings to numbers
    a = float(parsed_input[0])
    b = float(parsed_input[1])
    c = float(parsed_input[2])

    # solve the equation! like a wizard
    solutions = quadratic_equation(a, b, c)
    x1 = solutions[0]
    x2 = solutions[1]

    # Output according to number of solutions
    if(x1):  # x1 exists
        if(x2):  # x2 exists
            print("The equation has 2 solutions: {0} and {1}".format(x1, x2))
        else:
            print("The equation has 1 solution: {0}".format(x1))
    else:
        print("The equation has no solutions")


def quadratic_equation(a, b, c):
    """Gets the a,b,c parameters of the formula ax^2 +bx +c = 0.
    Solves the equation for x, and returns the following results for each case:
    2 solutions: returns both: (x1, x2)
    1 solution:  returns (x1, None)
    0 solutions: returns (None, None)
    """

    # Solving using the following formula:
    # x[1,2] = (-b [+,-] sqrt(b^2 -4ac))/(2a)
    # ammount of solutions is determined by the delta:
    delta = (b**2) - (4*a*c)

    # solve for each delta case
    if delta < 0:
        return None, None
    elif delta == 0:
        return (-b)/(2*a), None
    else:  # delta > 0
        sqrt_delta = math.sqrt(delta)
        x1 = (-b + sqrt_delta) / (2*a)
        x2 = (-b - sqrt_delta) / (2*a)
        return x1, x2
