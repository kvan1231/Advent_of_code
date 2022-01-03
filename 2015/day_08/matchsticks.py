# https://adventofcode.com/2015/day/8


def part1(input_file='input.txt'):
    """
    Calculates the difference between the number of characters
    in the code representation of the string literal and the number
    of characters in the in-memory string itself.
    """

    with open(input_file) as f:
        string_diff = sum(len(line) - len(eval(line)) for line in f)

    return string_diff


def part2(input_file='input.txt'):
    """
    Counts the number of \\ and " characters
    """

    with open(input_file) as f:
        enc_string_count = sum(
            2 + line.count('\\') + line.count('"') for line in f
        )

    return enc_string_count


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    p1_sol = part1()
    p2_sol = part2()

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
