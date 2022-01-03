# https://adventofcode.com/2021/day/25

import numpy as np


def read_data(input_file='test.txt'):
    """
    Reads in the data and converts it to an numpy array
    """

    # read in the raw data
    raw_data = np.genfromtxt(input_file, dtype='str')

    # split each row into the individual characters and keep is at np array
    data_array = np.array(
        list(map(list, raw_data))
    )

    return data_array


def sim_movement(input_array):
    """
    Use numpy roll to simulate the movement of the sea cucumbers
    in the input array where possible.
    """

    init_array = input_array.copy()
    steps = 0

    # create a list to keep track of whether or not the sea cucumbers can move
    can_move = [True]

    # if either of the last two commands let us move (east/south) then continue
    while any(can_move[-2:]):
        steps += 1
        
        for direction, axis in ((">", 1), ("v", 0)):
            # check the sea cucumber moves
            possible_move = (
                np.roll(init_array, -1, axis) == "."
            ) & (init_array == direction)

            # append True/False if any of the sea cucumbers can move
            can_move.append(np.any(possible_move))

            # update the old positions with empty space
            init_array[possible_move] = "."

            # update the new positions with the direction
            init_array[np.roll(possible_move, 1, axis)] = direction

    return steps


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    test_data = read_data()
    p1_test = sim_movement(test_data)

    data = read_data(input_file="input.txt")
    p1_sol = sim_movement(data)

    print("\nTests")
    print("=======")
    print("Part 1: ", p1_test)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
