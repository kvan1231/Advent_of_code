# https://adventofcode.com/2015/day/11

import string


def read_data(input_file='input.txt'):
    """
    Read in the password
    """

    with open(input_file) as f:
        raw_data = f.read()

    return raw_data


def rule1(pw):
    """
    Passwords must include one increasing straight of at least
    three letters, like abc, bcd, cde, and so on, up to xyz.
    They cannot skip letters; abd doesn't count.
    """

    # get the entire alphabet in lowercase
    alphabet = string.ascii_lowercase

    # loop through the word
    for ind in range(len(pw) - 2):
        # are 3 letters in consecutive order?
        if pw[ind: ind+3] in alphabet:
            return True
    return False


def rule2(pw):
    """
    Passwords may not contain the letters i, o, or l, as these
    letters can be mistaken for other characters and are therefore
    confusing.
    """
    letter_chk = all((char not in pw for char in 'iol'))

    return letter_chk


def rule3(pw):
    """
    Passwords must contain at least two different, non-overlapping
    pairs of letters, like aa, bb, or zz.
    """

    # initialize the number of pairs
    num_pair = 0
    skip = False

    # loop through the password
    for ind in range(len(pw) - 1):
        # if we're skipping next letter
        if skip:
            # flip boolean, continue
            skip = False
            continue

        # if we have a pair
        if pw[ind] == pw[ind + 1]:
            # increase num of pairs
            num_pair += 1
            # skip next character
            skip = True

    return num_pair > 1


def iter_pw(pw):
    """
    Iterates the characters in the password
    """

    pw_list = list(pw)
    # loop through the indices in the pw_list going backwards
    for pw_ind in range(len(pw_list) - 1, -1, -1):
        cur_letter = ord(pw_list[pw_ind])
        new_letter = chr(
            (cur_letter - ord('a') + 1) % 26 + ord('a')
        )
        pw_list[pw_ind] = new_letter
        if pw_list[pw_ind] != 'a':
            break

    # return the string
    return ''.join(pw_list)


def new_pw(pw):
    """
    Takes an input password and finds the new password
    that satisfies the rules.
    """

    # group the rules together
    all_rules = [rule1, rule2, rule3]

    # while not all rules are satsified
    while not all((rule(pw) for rule in all_rules)):
        # iterate the pw
        pw = iter_pw(pw)

    # return the pw once we've satisfied all conditions
    return pw


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    pw = read_data()
    p1_pw = new_pw(pw)
    p2_pw = new_pw(iter_pw(p1_pw))

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_pw)
    print("Part 2: ", p2_pw)
