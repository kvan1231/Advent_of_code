# https://adventofcode.com/2015/day/10

from itertools import groupby


def look_say(input_file='input.txt', n_iters=40):
    """
    Reads in an input file, applies the number of iterations
    given and outputs the length of the string.
    """

    # read in the file
    with open(input_file) as f:
        input_string = f.read()

    # loop through the number of iterations
    for iteration in range(n_iters):
        # generate the new string
        input_string = ''.join(
            [str(len(list(nums))) + str(val) for val,
                nums in groupby(input_string)]
        )

    # calculate the length of the string
    len_string = len(input_string)

    return len_string


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    p1_sol = look_say()
    p2_sol = look_say(n_iters=50)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
