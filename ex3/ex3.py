#!/usr/bin/env python3
#############################################################
# FILE : ex3.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex3 2016-2017
# DESCRIPTION: An exercise about loops and lists
#############################################################
import math


def create_list():
    """
    Reads multiple inputs from the user.
    Creats a list of all the inputs given until an empty string was recieved.
    Returns a list of all the inputs prior to the empty string.
    """
    inputs_list = []
    user_input = input()
    while user_input != "":
        inputs_list.append(user_input)
        user_input = input()

    return inputs_list


def concat_list(str_list):
    """
    Gets a list of strings.
    Concatenates all the strings to a single string (no spaces or seperators).
    Returns the concatenated list.
    """
    concated_list = ""
    for string in str_list:
        concated_list += string
    return concated_list


def average(num_list):
    """
    Gets a list of numbers.
    Calculates and returns their average as a float.
    """
    if len(num_list) == 0:
        return None
    else:
        sum = 0
        for num in num_list:
            sum += num
        average = float(sum / len(num_list))
        return average


def cyclic(lst1, lst2):
    """
    Checks if 2 lists are a cyclic permutation of each other
    Returns true if they are, otherwise false.
    """

    # Lists with different lengths cannot be cyclic permutaions
    if len(lst1) != len(lst2):
        return False

    # Two empty lists are a cyclic permutation
    if len(lst1) == 0:
        return True

    # Compare lst2 against all possible cyclic permutations of lst1 until a
    # match is found (or not)
    cycle_found = False
    for i in range(len(lst1)):
        shifted_lst1 = cyclic_shift(lst1, i)
        if (shifted_lst1 == lst2):
            cycle_found = True
            break

    return cycle_found


def cyclic_shift(list, shift):
    """
    Gets a list and an integer (shift)
    moves each item in the list <shift> steps forward, in a cyclic manner.
    """
    return list[-shift:] + list[:-shift]


def histogram(n, num_list):
    """
    Gets a non-negative integer (n) and a list of non negative numbers
    between 0 and n-1 (num_list).
    Returns a list of occurrences of each number in the range where the index
    symbloises the number counted, and the value is the actual count of
    occurrences.
    """
    # Initialize an empty histogram for all the numbers 0-(n-1)
    histogram = [0]*n

    # Count occurences for every number in the list
    for num in num_list:
        histogram[num] += 1

    return histogram


def prime_factors(n):
    """
    Gets an integer (n) greater or equal to 1.
    Returns a list of all the prime factors of that integer (so that
    multiplying all the factors in that list gives back the number. That
    implies repitions are possible).
    """
    # Create a list of all prime numbers lesser than or equal to n (potential
    # candidates for being it's factors)
    prime_candidates = []
    for num in range(2, n+1):
        if is_prime(num):
            prime_candidates.append(num)

    # Check which primes are actually factors of n, add them to the list
    prime_factors = []
    for prime in prime_candidates:
        while n % prime == 0:
            prime_factors.append(prime)
            n = n / prime

    return prime_factors


def is_prime(num):
    """
    Gets a number and returns wether it's prime or not.
    """
    if(num == 2):
        return True

    # Scan for factors of num between 2 and its root (rounded up)
    for factor in range(2, math.ceil(math.sqrt(num))):
        if num % factor == 0:
            return False

    # No factors at all? Prime!
    return True


def cartesian(lst1, lst2):
    """
    Gets 2 lists - lst1, lst2
    Returns a new list who's members are all the possible combinations of the
    form (lst1_item, lst2_item)
    """
    cartesian_list = []
    for lst2_item in lst2:
        for lst1_item in lst1:
            cartesian_list.append((lst1_item, lst2_item))
    return cartesian_list


def pairs(n, num_list):
    """
    Gets a number (n) and a list of numbers (num_list)
    Returns a new list, containing all the possible lists of 2 numbers who's
    sum is the number n.
    """
    sum_n_list = []
    # For each number in the list, look forward through all the numbers
    # proceeding it and check if their sum is n.
    for i in range(len(num_list)):
        for j in range(len(num_list) - (i+1)):
            if (num_list[i] + num_list[(i+1) + j] == n):
                sum_n_list.append([num_list[i], num_list[i+j+1]])
    return sum_n_list
