#!/usr/bin/env python3
#############################################################
# FILE : ex4.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex4 2016-2017
# DESCRIPTION: A Pythonic version Of The Game Hangman
#############################################################
from hangman_helper import *
import string

VALID_LETTERS_LIST = list(string.ascii_lowercase)
HIDDEN_LETTER = "_"

def should_play_again():
    """
    Asks the user if he wants to play again.
    Returns True if he does, otherwise False.
    """
    input_type, input_value = get_input()
    if (input_type == PLAY_AGAIN):
        return input_value  # True/False
  
    # Oops, wrong input type...
    return False
  

def update_word_pattern(word, pattern, letter):
    """
    Gets a word (str), A letter (chr), And a pattern (str) - all in lowercase.
    The pattern must be of the same length as the word.
    The pattern is composed of underscores '_' representing hidden 
    letters in the word, and 'visible' letters of the word (lowercase alphabet).
    The function checks where the given letter occurs in the word, and
    Returns a new, updated pattern with the occurrences of the letter now 
    visible.
    Example:
       update_word_pattern('apple', '___l_', 'p')
       --> '_ppl_'
    """
    # Validate lowercase
    word = word.lower()
    pattern = pattern.lower()
    letter = letter.lower()
  
    # Create an updated version of pattern as a list
    updated_pattern = list(pattern)

    # List all the positions of letter in word
    letter_positions = []
    for (position, char) in enumerate(word):
        if char == letter:
            letter_positions.append(position)

    # Reveal all the occurrences of the letter in updated pattern 
    # (replace '_' with letter)  
    for position in letter_positions:
        updated_pattern[position] = letter

    # Return the updated pattern as an str
    return "".join(updated_pattern)


def is_valid_letter(letter):
    """
    Returns wether the given letter is a valid input, i.e:
    exactly 1 character of lowercase alphabet.
    """
    return letter in VALID_LETTERS_LIST


def run_single_game(word_list):
    """
    Run a single game of Hangman.
    Gets a list of words to choose the game-word from.
    Chooses a random word from the list and prompts the user to keep guessing 
    letters until the word is discovered, or the turns run out.
    Win/Lose is announced after game is over, and the user can choose to play
    """
    # Init the game
    secret_word = get_random_word(word_list)
    pattern = HIDDEN_LETTER * len(secret_word)
    error_count = 0
    wrong_guess_lst = []
    msg = DEFAULT_MSG 

    # Take guesses until word is discovered or guess limit reached
    while ((pattern != secret_word) and (error_count < MAX_ERRORS)):
        # Update display and prompt for input
        display_state(pattern, error_count, wrong_guess_lst, msg, ask_play=False)
        input_type, input_value = get_input()
        # Input was a guess
        if input_type == LETTER:
            letter = input_value
            # Validate legal guess
            if (not is_valid_letter(letter)):
                msg = NON_VALID_MSG
                continue
            # Validate not repeating guess
            elif (letter in pattern) or (letter in wrong_guess_lst):
                msg = ALREADY_CHOSEN_MSG + letter
            # Good guess: Update pattern
            elif letter in secret_word:
                pattern = update_word_pattern(secret_word, pattern, letter)
                msg = DEFAULT_MSG
            # Wrong guess: Update errors count and bad guesses list
            else:  # Valid but wrong guess 
                wrong_guess_lst.append(letter)
                error_count += 1
                msg = DEFAULT_MSG
        # Input was hint request
        elif input_type == HINT:
            # Find and return the most common letter in the words that still make sense 
            filtered_words = filter_words_list(word_list, pattern, wrong_guess_lst)
            letter_hint = choose_letter(filtered_words, pattern)
            msg = HINT_MSG + letter_hint

    # Check if the player won or ran out of guesses
    if (pattern == secret_word):
        msg = WIN_MSG
    else:  # error count >= MAX_ERRORS
        msg = LOSS_MSG + secret_word

    # Display score and ask to play again
    display_state(pattern, error_count, wrong_guess_lst, msg, ask_play=True)


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    Gets a list of words (str list), a list of letters (char list) and a pattern
    (str).
    Returns a new list of all the word from the original list which match the 
    pattern and don't contain any of the wrong letters.
    Example:
        words = ['mat', 'cat', 'rat', 'car']
        pattern = '__t'
        wrong_guess_lst = ['m', 'n', 'l']
        returns ['cat', 'rat']
    """ 
    is_candidate = lambda word: is_word_a_candidate(word, pattern, wrong_guess_lst)
    return list(filter(is_candidate, words))


def is_word_a_candidate(word, pattern, bad_chars):
    """
    Returns if a word matches a given pattern, and contains no bad chars.
    Example:
        pattern = '__t'
        bad_chars = ['m', 'n', 'l']
        'flat' : False (bad length)
        'mat'  : False (contains bad char 'm')
        'car'  : False (doesn't match pattern)
        'cat'  : True
    """
    # Validate same lengths
    if len(word) != len(pattern):
        return False
  
    for i in range(len(word)):
        # Validate word matches pattern where not '_'
        if (pattern[i] != HIDDEN_LETTER and word[i] != pattern[i]):
            return False
        # Validate rest of the word contains no bad chars
        elif (word[i] in bad_chars):
            return False
  
    # Reaching here means the word is legit
    return True


def choose_letter(words, pattern):
    """
    Returns the most common letter in a list of words which does not appear 
    in the pattern.
    The words must only contain valid letters. 
    """
    # Generate dictionary of occurrences per each valid letter
    histogram = dict(zip(VALID_LETTERS_LIST, [0]*len(VALID_LETTERS_LIST)))
    for word in words:
        for letter in word:
            histogram[letter] += 1
  
    # Remove all the letters which already appeared in the pattern by setting
    # their value to -1 (which is smaller than 0).
    NOT_IN_HISTOGRAM = -1
    for letter in pattern: 
        if (letter in VALID_LETTERS_LIST):
            histogram[letter] = NOT_IN_HISTOGRAM
      
    # Return the letter with the largest corresponding number of occurences
    return max(histogram, key=histogram.get)


def main():
    # Read the list of words and start playing
    words_list = load_words()
    keep_playing = True
    
    # Play until users wants to stop
    while keep_playing:
        run_single_game(words_list)
        keep_playing = should_play_again()


if __name__ == "__main__":
    start_gui_and_call_main(main)
    close_gui()