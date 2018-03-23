#!python3
#############################################################
# FILE : largest_and_smallest.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module for finding the largest and smallest
# of 3 given numbers
#############################################################


def largest_and_smallest(num1, num2, num3):
    """Gets 3 numbers. Returns 2 numbers: (largest, smallest)."""
    largest = num1
    smallest = num1

    if num2 > largest:
        largest = num2
    elif num2 < smallest:
        smallest = num2

    if num3 > largest:
        largest = num3
    elif num3 < smallest:
        smallest = num3

    return largest, smallest