# https://adventofcode.com/2021/day/19

import numpy as np
import math
from itertools import combinations


def read_data(input_file='test.txt'):
    """
    This function will read in the input data and output
    the coordinates of the sensors
    """

    # read in the raw data
    data = open(input_file).read()

    # initialize the list to contain the beacon coords
    beacons = data.split("\n\n")

    # split it at each new beacon
    beacons = [line.split("---\n")[-1].split("\n") for line in beacons]

    beacons = [
        np.array(
            [list(map(int, coord.split(','))) for coord in line]
        ) for line in beacons
    ]

    return beacons


def permute_orientations():
    """
    Generate all possible orientations and return it
    """
    directions = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    directions = list(map(np.array, directions))
    for x_vec in directions:
        for y_vec in directions:
            if x_vec.dot(y_vec) == 0:
                z_vec = np.cross(x_vec, y_vec)
                yield lambda rot_array: np.matmul(
                    rot_array, np.array([x_vec, y_vec, z_vec])
                )


def gen_dist_set(coordinates):
    """
    Generate a set of sorted absolute coordinate differences
    between pairs of points
    """
    dist_set = {
        tuple(
            sorted(
                map(
                    abs, coordinates[i, :] - coordinates[j, :]
                )
            )
        ): (i, j) for i, j in combinations(range(len(coordinates)), 2)
    }
    return dist_set


def fit_beacons(beacon, dists, b_ind1, b_ind2, d_ind):
    """
    Find the correct rotation/translation to make beacon b_ind2 match with
    beacon b_ind2
    """
    beacon1, beacon2 = beacon[b_ind1], beacon[b_ind2]

    # loop through the permutations of a given beacon
    for rotation in permute_orientations():
        rot_beacon2 = rotation(beacon2)

        # check distances
        sub_dist = dists[b_ind1][d_ind][0]

        # calculate the differences
        for dist_val in dists[b_ind2][d_ind]:
            diff = beacon1[sub_dist, :] - rot_beacon2[dist_val, :]

            # find the the unique beacons
            b1_tuple = set(map(tuple, beacon1))
            b2_tuple = set(map(tuple, rot_beacon2 + diff))

            if len((b_overlap := b2_tuple) & b1_tuple) >= 12:
                return diff, b_overlap, rotation


def match_beacons(beacons, dists):
    """
    Determine which scanners have overlap
    """

    num_dists = len(dists)
    for ind1, ind2 in combinations(range(num_dists), 2):
        dist_set1 = set(dists[ind1])
        dist_set2 = set(dists[ind2])
        common_dist = dist_set1 & dist_set2

        if len(common_dist) >= math.comb(12, 2):
            yield ind1, ind2, next(iter(common_dist))


def solve_beacons(beacons):
    """
    Take a list of beacons and return a set of positions and beacons
    """

    beacon_copy = beacons.copy()
    beacon_position = {0: (0, 0, 0)}
    dists = list(map(gen_dist_set, beacon_copy))
    init_beacon = set(map(tuple, beacon_copy[0]))

    while len(beacon_position) < len(beacon_copy):
        for b_ind1, b_ind2, d_ind in match_beacons(beacon_copy, dists):
            if not (b_ind1 in beacon_position) ^ (b_ind2 in beacon_position):
                continue
            elif b_ind2 in beacon_position:
                b_ind1, b_ind2 = b_ind2, b_ind1
            beacon_position[b_ind2], new_beacon, rotation = fit_beacons(
                beacon_copy, dists, b_ind1, b_ind2, d_ind
            )
            beacon_copy[b_ind2] = rotation(beacon_copy[b_ind2]) +\
                beacon_position[b_ind2]
            init_beacon |= new_beacon
    return [beacon_position[b_ind] for b_ind in range(len(beacon_copy))], init_beacon


def p1_pipeline(input_file='test.txt'):
    # input_file = 'test.txt'
    data = read_data(input_file)
    beacon_pos, beacons = solve_beacons(data)
    num_beacons = len(beacons)

    max_dist = max(
        np.abs(xpos - ypos).sum() for xpos, ypos in combinations(beacon_pos, 2)
    )

    print("part 1:", num_beacons)
    print("part 2:", max_dist)


p1_pipeline()
p1_pipeline("input.txt")
