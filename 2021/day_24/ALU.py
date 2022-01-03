# https://adventofcode.com/2021/day/24
# this problem was solved following a tutorial
# https://github.com/mebeim/aoc/blob/master/2021/README.md#advent-of-code-2021-walkthrough


from collections import deque
from functools import reduce


def read_data(input_file='input.txt'):
    """
    Read in the data and convert it into an iterator
    """

    with open(input_file) as f:
        raw_data = f.read()

    # split it into a list
    raw_commands = [line for line in raw_data.split('\n')]
    # convert it to an iterator
    commands = iter(raw_commands)
    return commands


def skip_cmds(cmds, num_lines):
    """
    This function will iterate through our commands to skip lines
    """
    for _ in range(num_lines):
        next(cmds)


def generate_number(input_cmds):
    """
    This function takes in the input commands that should generate at 14 digit
    number where each digit ranges from 1-9. The input commands should be 14
    different 18 command chunks where each chunk consists of similar 18
    commands.
    """

    output_num = []
    stack = deque()

    # loop through th 14 digits
    for digit in range(14):

        # skip the first 4 commands
        skip_cmds(input_cmds, 4)

        # remove the trailing whitespace
        cmd = next(input_cmds).rstrip()

        # make sure the command is where we think it is
        assert cmd.startswith("div z "), 'Invalid Input'

        if cmd == 'div z 1':
            skip_cmds(input_cmds, 10)
            cmd = next(input_cmds)

            # make sure the command is where we think it is
            assert cmd.startswith("add y "), 'Invalid Input'

            div_val = int(cmd.split()[-1])
            stack.append((digit, div_val))
            skip_cmds(input_cmds, 2)

        else:
            cmd = next(input_cmds)

            # make sure the command is where we think it is
            assert cmd.startswith("add x"), "Invalid Input"

            val = int(cmd.split()[-1])
            temp_digit, temp_val = stack.pop()
            output_num.append((digit, temp_digit, temp_val + val))
            skip_cmds(input_cmds, 12)

    return output_num


def find_lims(output_nums):
    """
    Find the maximum and minimum value in our outputs
    """

    # initialize the max and min digits
    max_digits = [0] * 14
    min_digits = [0] * 14

    # solve for the pairs of digits
    for ind1, ind2, diff in output_nums:
        if diff > 0:
            max_digits[ind1], max_digits[ind2] = 9, 9 - diff
            min_digits[ind1], min_digits[ind2] = 1 + diff, 1
        else:
            max_digits[ind1], max_digits[ind2] = 9 + diff, 9
            min_digits[ind1], min_digits[ind2] = 1, 1 - diff

    # reduce the digit lists to a single number
    max_digits = reduce(lambda ind, digit: ind * 10 + digit, max_digits)
    min_digits = reduce(lambda ind, digit: ind * 10 + digit, min_digits)

    return max_digits, min_digits


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    data = read_data()
    output_nums = generate_number(data)
    p1_sol, p2_sol = find_lims(output_nums)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
