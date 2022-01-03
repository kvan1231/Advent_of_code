# https://adventofcode.com/2021/day/24
# this problem was solved following a tutorial
# https://github.com/mebeim/aoc/blob/master/2021/README.md#advent-of-code-2021-walkthrough


def read_data(input_file='input.txt'):
    """
    Read in the data and split it into a list
    """

    with open(input_file) as f:
        raw_data = f.read()

    commands = [line.split() for line in raw_data.split('\n')]
    return commands


