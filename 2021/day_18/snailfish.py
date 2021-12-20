# https://adventofcode.com/2021/day/18

from itertools import permutations


def read_data(input_file='test.txt'):
    """
    This function will read in the input file and convert it into
    a list of lists
    """
    data = open(input_file).read()
    data_list = [eval(line) for line in data.split("\n")]
    init_list = data_list[0]
    subsequent_snailfish = data_list[1:]
    return data_list, init_list, subsequent_snailfish


def add_(left, right, side='l'):
    """
    The snailfish addition operator that combines the two
    pairs involved in the operation
    """

    # if theres no right hand term then just return the left term
    if not right:
        return left

    # if the right hand term is an integer then just add it to the pair
    if type(left) == int:
        return left + right

    # if its left handed or right handed addition then combine the pairs
    # at the appropriate level
    if side == 'l':
        return [add_(left[0], right, side='l'), left[1]]
    if side == 'r':
        return [left[0], add_(left[1], right, side='r')]


def explode_pairs(pair, layer):
    """
    This function explodes a pair where the pair's left value is added to the
    first regular number to the left of the exploding pair if any. The right
    value is added to the first regular number to the right. Exploding pairs
    will always consist of two regular numbers. The entire exploding pair is
    replaced with the regular number 0.
    """

    # replace the exploding pair with 0
    if type(pair) == int:
        return False, pair, 0, 0

    # split the pair into the values
    left_val, right_val = pair

    # if we're in the 4th layer then we're exploding values
    if layer == 4:
        return True, 0, left_val, right_val

    # explode the left pair
    exploded, nxt, left, right = explode_pairs(left_val, layer+1)
    if exploded:
        return True, [nxt, add_(right_val, right, side='l')], left, 0

    # explode the right pair
    exploded, nxt, left, right = explode_pairs(right_val, layer+1)
    if exploded:
        return True, [add_(left_val, left, side='r'), nxt], 0, right

    return False, pair, 0, 0


def split_numbers(pair):
    """
    If a value in a pair is greater than 9 then we're going to split it
    half
    """

    # If the pair is an integer
    if type(pair) == int:
        if pair > 9:
            # split the pair and the right value will be greater
            return [pair // 2, pair // 2 + (pair & 1)]
        # if its not greater than 9 then just return it
        return pair

    left_val, right_val = pair
    left = split_numbers(left_val)
    if left != left_val:
        return [left, right_val]
    return [left, split_numbers(right_val)]


def add_snailfish(left, right):
    """
    This function should add up all of the snailfishes
    """

    result = [left, right]

    # Loop through the values
    while True:

        # explode a pair
        exploded, result, _, _ = explode_pairs(result, 0)
        if not exploded:
            # check the pair
            previous_pair = result
            result = split_numbers(result)
            if result == previous_pair:
                return result


def calc_magnitude(pair):
    if type(pair) == int:
        return pair
    return 3 * calc_magnitude(pair[0]) + 2 * calc_magnitude(pair[1])


def snailfish_pipeline(input_file='test.txt'):
    data_list, init_line, subsequent_snailfish = read_data(input_file)
    for line in subsequent_snailfish:
        init_line = add_snailfish(init_line, line)
    p1_val = calc_magnitude(init_line)

    p2_val = 0
    for left, right in permutations(data_list, 2):
        init_line = add_snailfish(left, right)
        p2_val = max(p2_val, calc_magnitude(init_line))
    print("part 1:", p1_val)
    print("part 2:", p2_val)


snailfish_pipeline()
snailfish_pipeline('input.txt')
