#!/usr/bin/env python3
#############################################################
# FILE :        ex7.py
# WRITER :      Raz Karl , razkarl , 311143127
# EXERCISE :    intro2cs ex7 2016-2017
# DESCRIPTION:  Create a mosaic of a picture from a set of
#               of images.
#############################################################


def print_to_n(n):
    """
    @brief      Prints all the integers up to n in ascending order
    
    @param      n   Integer - last number to print
    """
    if (n > 0):
       
        if (n > 1):
            print_to_n(n-1)

        print(n)


def print_reversed(n):
    """
    @brief      Prints all the integers up to n in descending order
    
    @param      n   Integer - number to start printing from
    """
    if (n > 0):
       
        print(n)
        
        if (n > 1):
            print_reversed(n-1)


def is_prime(n):
    """
    @brief      Checks if an integer (n) is prime
    
    @param      n   Integer - test subject
    
    @return     True if prime, False otherwise
    """
    if (n < 2):
        return False

    if (n == 2):
        return True

    # Divisors larger than the root always team up with divisors smaller than
    # the root, so searching only below the root yields the same results, 
    # just faster!
    round_root_n = n // (n**(1/2))  # calculates the integer part of the root
    
    return not has_divisor_smaller_than(n, round_root_n)


def has_divisor_smaller_than(n, i):
    """
    @brief      Determines if n has a positive integer divisor smaller than i 
                (other than 1)
    
    @param      n   Integer - divison subject
    @param      i   Integer - divisor candidate
    
    @return     True n has a positive integer divisor smaller than i (other 
                than 1), False otherwise.
    """
    if (i < 2):
        return False

    if (n % i == 0):
        return True

    return has_divisor_smaller_than(n, i-1)


def divisors(n):
    """
    @brief      Returns a list of all positive integers dividing n.
    
    @param      n   Integer - divison subject
    
    @return     A list of all positive integers dividing n.
    """
    if (n < 0):
        n = -n

    if (n < 1):
        return []

    return list_divisors_smaller_than(n, n)


def list_divisors_smaller_than(n, i):
    """
    @brief      Lists all positive integer divisors of n below i
    
    @param      n   Integer - division subject
    @param      i   Integer - divisor candidate
    
    @return     A list of all positive integer divisors of n below i
    """
    if (i <= 1):
        return [1]

    if (n % i == 0):
        return list_divisors_smaller_than(n, i-1) + [i]

    return list_divisors_smaller_than(n, i-1)


def exp_n_x(n,x):
    """
    @brief      Reurns an approximation of e^x
                Calculates the sum of (x^i / i!) for i:0->n
    
    @param      n   Integer - meausrement of approximation (larger values yield 
                              more accurate results)
    @param      x   Float   - power of e
    
    @return     An approximation of e^x
    """
    if (n == 0):
        return 1
    
    return power_over_factorial(x, n) + exp_n_x(n-1, x)


def power_over_factorial(x,n):
    """
    @brief      Calculates (x^n / n!)
    
    @param      x   Integer - will be raised to the n'th power 
    @param      n   Integer - factorial subject and power of x
    
    @return     x^n / n!
    """
    if (n <= 1):
        return x
    
    return (x / n) * power_over_factorial(x, n-1)


def play_hanoi(hanoi, n, src, dest, temp):
    """
    @brief      Solves the game of hanoi for the given setup
                See hanoi_game.py for classes documentation
    
    @param      hanoi  Hanoi class - GUI for animated towers-of-Hanoi-game with
                                     upto 10 discs
    @param      n      Integer     - number of discs to move
    @param      src    Tower class - the tower from which discs are moved
    @param      dest   Tower class - the tower to which discs are moved
    @param      temp   Tower class - tower for temporarily holding moved dics
    """
    if (n < 1):
        return

    if (n == 1):
        hanoi.move(src, dest)
        return

    play_hanoi(hanoi, n-1, src, temp, dest)
    hanoi.move(src, dest)
    play_hanoi(hanoi, n-1, temp, dest, src)


def print_binary_sequences(n):
    """
    @brief      Prints all possible n-characters-long string combinations of '0'
                and '1' (repitions allowed)
    
    @param      n     Integer - length of the strings
    """
    print_sequences(['0', '1'], n)


def print_sequences(char_list, n):
    """
    @brief      Prints all possible n-characters-long string combinations of 
                characters from the list (repitions allowed)
    
    @param      char_list  chr list - list of characters (all different)
    @param      n          Integer  - length of the srings
    """
    print_sequences_with_prefix(char_list, n, "")


def print_sequences_with_prefix(char_list, n, prefix):
    """
    @brief      Prints all possible n-characters-long string combinations of 
                the given prefix with characters from the list (repitions 
                allowed)
    
    @param      char_list  List     - list of characters (all different)
    @param      n          Integer  - length of the srings
    @param      prefix     String   - the prefix of the sequence
    """
    if (n <= 0):
        print(prefix)
        return

    # Print all sequences starting with the prefix followed by a single 
    # character from the list
    for char in char_list:
        prefix_with_char = prefix + char
        print_sequences_with_prefix(char_list, n-1, prefix_with_char)


def print_no_repetition_sequences(char_list, n):
    """
    @brief      Prints all possible n-characters-long string combinations of 
                the given prefix with characters from the list (no repitions 
                allowed)
    
    @param      char_list  List     - list of characters (all different)
    @param      n          Integer  - length of the srings
    """
    for sequence in no_repetition_sequences_list(char_list, n):
        print(sequence)


def no_repetition_sequences_list(char_list, n):
    """
    @brief      Reutrns a list of all possible n-characters-long string 
                combinations of characters from the list, with no repitions.
    
    @param      char_list  List     - list of characters (all different)
    @param      n          Integer  - length of the srings
    """
    return no_rep_seq_list_with_prefix(char_list, n, "")


def no_rep_seq_list_with_prefix(char_list, n, prefix):
    """
    @brief      Reutrns a list of all possible n-characters-long string 
                combinations of characters from the list starting with the given
                prefix, with no repeating characters.
    
    @param      char_list  List     - list of characters (all different, none is
                                      in the prefix)
    @param      n          Integer  - length of the srings
    @param      prefix     String   - the preix of the sequence
    """
    if (n < 0):
        return []

    if (n == 0):
        return [prefix]

    # Generate all possible sequences starting with the prefix followed by a 
    # single character from the list
    all_possible_sequences = []
    for char in char_list:
        rest_of_chars    = list_without_item(char_list, char)
        prefix_with_char = prefix + char
        sequences_with_char = no_rep_seq_list_with_prefix(rest_of_chars, 
                                                          n-1, 
                                                          prefix_with_char)
        for sequence in sequences_with_char:
            all_possible_sequences.append(sequence)

    return all_possible_sequences


def list_without_item(lst, item):
    """
    @brief      returns a new list identical to the origianl without the
                specified item
    
    @param      lst   The list to copy
    @param      item  The item to remove
    
    @return     A new list identical to the origianl without the
                specified item.
    """
    new_lst = list(lst)
    new_lst.remove(item)
    return new_lst