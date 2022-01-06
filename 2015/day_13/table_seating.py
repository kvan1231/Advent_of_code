# https://adventofcode.com/2015/day/13

from itertools import permutations
from collections import defaultdict
import re


def read_data(input_file='test.txt'):
    """
    Read in the data and return it as a list
    """

    with open(input_file) as f:
        raw_data = f.read()

    # split it into a list
    data_list = [line for line in raw_data.split('\n')]

    return data_list


def gen_seating(input_list, add_self=False):
    """
    Takes an input_list that contains the different seating positions
    and the happiness of each person in that position. It then calculates
    the total happiness of that seating configuration and stores it.
    """

    # initialize the seating dictonary
    seating = defaultdict(dict)

    for line in input_list:

        # we're using regex to pull the data
        temp_line = re.match(
            r'(\S+) would (lose|gain) (\d+) happiness units by sitting next to (\S+)\.',
            line
        )

        # pull person1, sign (pos/neg), val (value of change) and person2
        pers1, sign, val, pers2 = temp_line.group(1, 2, 3, 4)

        # add the happiness levels in the seating dictonary
        if sign == 'gain':
            seating[pers1][pers2] = int(val)
        elif sign == 'lose':
            seating[pers1][pers2] = -int(val)

    if add_self:
        for person in list(seating.keys()):
            seating['me'][person] = 0
            seating[person]['me'] = 0

    # loop through all permutations
    happiness = []
    for people in permutations(seating.keys()):
        temp_happy = sum(
            seating[p1][p2] + seating[p2][p1] for p1, p2 in zip(
                people, people[1:]
            )
        )
        temp_happy += seating[people[0]][people[-1]] + \
            seating[people[-1]][people[0]]
        happiness.append(temp_happy)

    max_happy = max(happiness)
    return max_happy


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    test_data = read_data()
    p1_test = gen_seating(test_data)

    print("\nTests")
    print("=======")
    print("Part 1: ", p1_test)

    data = read_data("input.txt")
    p1_sol = gen_seating(data)
    p2_sol = gen_seating(data, add_self=True)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
