#!python3
#############################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module to help Hermiony with her friends'
# math homework
#############################################################
import math


def is_valid_num(num, name):
    """Gets a number parameter and it's name.
    Returns True if the parameter is a valid number,
    otherwise prints an error message and returns False."""
    if (type(num) not in [int, float]):
        print("{0} has an invalid type ('{1}', of type {2}), expected (int)" /
              "or (float).".format(name, num, type(num)))
        return False
    return True


def calculate_mathematical_expression(num1, num2, operation):
    """Gets 2 numbers and a mathematical operation ('+','-','*','/').
    Returns the result of applying the operation on the 2 numbers in the given
    order.
    If the operation fails (bad number type, unrecognized operation or division
    by 0) returns None.
    """

    # Validate number parameters
    if (not is_valid_num(num1, "num1") or not is_valid_num(num2, "num2")):
        return None

    # Parse operation and calculate!
    if (operation == '+'):
        return num1 + num2

    elif (operation == '-'):
        return num1 - num2

    elif (operation == '*'):
        return num1 * num2

    elif (operation == '/'):
        if (num2 == 0):
            # print("Cannot divide by zero ({0} / {1}).".format(num1, num2))
            return None
        else:
            return num1 / num2
    else:  # invalid operation
        # print("invalid operation '{0}'. Expected ['+','-','*','/']".format(operation))
        return None


def calculate_from_string(expression):
    """Gets an expression string of the format '[num1] [operation] [num2]'.
    Returns the result of applying the operation on the 2 numbers in the given
    order.
    If the operation fails (bad number type, unrecognized operation or division
    by 0) returns None.
    Permitted operators: ('+','-','*','/')
    """

    # Parse the expression string and validate format
    parsed_expression = expression.split(' ')

    # Checks if the expression is parsed in the following format:
    #   [0] - string representing a number
    #   [1] - string representing an operator (can be anything)
    #   [2] - string representing a number
    if (len(parsed_expression) != 3):
        print("Bad number of arguments ({0})".format(len(parsed_expression)))
        return None
    s_num1 = parsed_expression[0]
    s_operation = parsed_expression[1]
    s_num2 = parsed_expression[2]

    # Carefully convert user input to floating point numbers
    try:
        num1 = float(s_num1)
    except:
        print("Invalid argument for num1 ({0})".format(s_num1))
        return None
    try:
        num2 = float(s_num2)
    except:
        print("Invalid argument for num1 ({0})".format(s_num2))
        return None

    return calculate_mathematical_expression(num1, num2, s_operation)
