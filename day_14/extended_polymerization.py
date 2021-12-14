# https://adventofcode.com/2021/day/14

from collections import Counter


def process_data(input_name="test.txt"):
    # read in the data
    init_polymer, pairs = open(input_name, 'r').read().split('\n\n')

    # create a dictionary to keep the pairs
    pair_dict = {}

    # generate the dictonary
    for pair in pairs.strip().split("\n"):
        poly_temp, pair_insert = pair.strip().split(" -> ")
        pair_dict[poly_temp] = pair_insert

    return init_polymer, pair_dict


def iterate_pairs(init_polymer, pair_dict, steps=10):
    """
    take the initial polymer, pair dictonary and number
    of steps to extend the initial polymer to a longer
    string and counts the letters
    """

    # Use the magic of collections.Counter to count the elements
    # count the initial polymer
    polymer_count = Counter(init_polymer)

    # count the pairs
    polymer_pairs = [
        a + b for a, b in zip(init_polymer, init_polymer[1:])
        ]
    pair_counts = Counter(polymer_pairs)

    # iterate through the steps
    for step in range(steps):
        # create a temp pair that we're going to update
        temp_pairs = pair_counts.copy()

        # loop through the input and outputs in the pair_dict
        for (init_1, init_2), out_val, in pair_dict.items():
            letter_count = temp_pairs[init_1 + init_2]
            pair_counts[init_1 + init_2] -= letter_count
            pair_counts[init_1 + out_val] += letter_count
            pair_counts[out_val + init_2] += letter_count
            polymer_count[out_val] += letter_count

    # find the most and least common letter
    most_common = polymer_count.most_common()[0][1]
    least_common = polymer_count.most_common()[-1][1]

    return polymer_count, most_common, least_common


init_polymer, pair_dict = process_data("input.txt")

p1_pc, p1_mc, p1_lc = iterate_pairs(init_polymer, pair_dict, steps=10)
p1_sol = p1_mc - p1_lc

print("part 1 solution:", p1_sol)

p2_pc, p2_mc, p2_lc = iterate_pairs(init_polymer, pair_dict, steps=40)
p2_sol = p2_mc - p2_lc

print("part 2 solution:", p2_sol)