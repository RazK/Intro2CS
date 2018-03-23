#!python3
#############################################################
# FILE : math_print.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex1 2016-2017
# DESCRIPTION: A set of functions which print mathematical
#############################################################

import math

def sin_30():
    """Prints the value of sin 30 radians."""
    print(math.sin(30))

def golden_ratio():
    """Prints the golden ration."""
    print((1 + math.sqrt(5))/2)

def square_five():
    """Prints 5 squared."""
    print(math.pow(5,2))

def hypotenuse(a=4, b=5):
    """Prints the hypotenuse in triangle with given side lengths."""
    print(math.sqrt(math.pow(a, 2) + math.pow(b, 2)))

def pi():
    """Prints a the ration between a circle's perimeter and it's diameter (Pi)."""
    print(math.pi)

def e():
    """Prints the root of the natural logarithm (e)"""
    print(math.e)

def squares_area(start=1, end=10):
    """Prints the areas of all the squares within a given range"""
    area = lambda x: int(math.pow(x, 2))
    for x in range(start, end):
        print(area(x), end=" ")
    print(area(x+1))

def main():
    sin_30()
    golden_ratio()
    square_five()
    hypotenuse()
    pi()
    e()
    squares_area()

if(__name__ == "__main__"):
    """Boilerplate for testing my code from a shell"""
    main()