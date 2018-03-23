#!python3
#############################################################
# FILE : convert_spoon_to_cup.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex2 2016-2017
# DESCRIPTION: A module to help Ron Wiezly with making
# poitions
#############################################################
import math

SPOONS_IN_CUP = 3.5


def convert_spoon_to_cup(spoons):
    """Gets an ammount of potion measured with spoons.
    returns the equivalent ammount measured with cups."""
    return spoons / SPOONS_IN_CUP
