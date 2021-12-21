# https://adventofcode.com/2015/day/5

import re


def find_nice_string(input_file='input.txt'):
    """
    This function reads in an input file which contains a list of strings.
    The first part of the function then defines if a string is nice or not
    based on certain rules:
        1. It contains at least three vowels
        2. It contains at least one letter that appears twice in a row
        3. It does not contain the strings ab, cd, pq, or xy

    The second part of the function then changes the rules of what is a nice
    string based on:
        1. It contains a pair of any two letters that appears at least twice
        in the string without overlapping
        2. It contains at least one letter which repeats with exactly one
        letter between them

    The function then returns the number of nice strings.
    """

    # read in the list of strings
    string_list = open("input.txt").read().strip().split()

    # find the nice strings that satisfy the rules
    nice_strings = [s for s in string_list if (
        # contains at least 3 vowels
        re.search(r'([aeiou].*){3,}', s) and
        # contains at least one letter that appears twice
        re.search(r'(.)\1', s) and
        # doesn't contain ab, cd, pq, or xy
        not re.search(r'ab|cd|pq|xy', s))
    ]

    better_strings = [s for s in string_list if (
        # contains a pair that appears twice without overlapping
        re.search(r'(..).*\1', s) and
        # contains at least one letter that repeats with a letter between
        re.search(r'(.).\1', s))
    ]

    # determine the number of nice strings and better strings
    num_nice_strings = len(nice_strings)
    num_better_strings = len(better_strings)

    # return values
    return num_nice_strings, num_better_strings


nice_strings, better_strings = find_nice_string()
print("Part 1: ", nice_strings)
print("Part 2: ", better_strings)
