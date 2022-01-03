# https://adventofcode.com/2015/day/9

from itertools import permutations
from collections import defaultdict


def read_data(input_file='test.txt'):
    """
    Read in the data and return it as a list
    """

    with open(input_file) as f:
        raw_data = f.read()

    # split it into a list
    data_list = [line for line in raw_data.split('\n')]

    return data_list


def gen_distances(input_list):
    """
    Takes an input_list and converts it into a series of origins,
    destinations and calculates the distances.
    """

    # initialize the location and distances
    locations = set()
    distances = defaultdict(dict)

    for line in input_list:
        # split the line into origin, destination and distance
        (origin, _, dest, _, dist) = line.split()

        # add our origins and destination to the location set
        locations.add(origin)
        locations.add(dest)

        # add to the distance dictionary
        distances[origin][dest] = int(dist)
        distances[dest][origin] = int(dist)

    # loop through all location permutations
    dist_list = []
    for places in permutations(locations):
        temp_dist = sum(
            map(
                lambda loc1, loc2: distances[loc1][loc2],
                places[:-1], places[1:]
                )
        )
        dist_list.append(temp_dist)

    shortest_dist = min(dist_list)
    longest_dist = max(dist_list)

    return shortest_dist, longest_dist


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    test_data = read_data()
    p1_test, p2_test = gen_distances(test_data)

    print("\nTests")
    print("=======")
    print("Part 1: ", p1_test)
    print("Part 2: ", p2_test)

    data = read_data("input.txt")
    p1_sol, p2_sol = gen_distances(data)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
