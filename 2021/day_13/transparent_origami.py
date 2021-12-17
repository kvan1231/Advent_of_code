# https://adventofcode.com/2021/day/13

import numpy as np
import matplotlib.pyplot as plt


# read in the data
def read_input(file_name="test.txt"):
    """
    This function should read in the data and process it into two
    outputs, the initial starting coordinates and the folding
    instructions
    """
    with open(file_name, 'r') as f:
        # there is a blank line between the coordinates
        # and the folding instructions
        coords, folds = f.read().split("\n\n")

    # convert the coordinates into a list
    coord_list = [
        [int(num) for num in line.split(",")] for line in coords.split("\n")
    ]

    # convert to numpy array
    coord_array = np.array(coord_list)

    # split the folds once
    fold_instructions = folds.strip().split("\n")

    # map the x and y in fold instructions to 1 or 0 for np.flip
    fold_axis_map = {"x": 1, "y": 0}

    # convert the instructions into coordinate and line number
    fold_coord = [(
        fold_axis_map[line.split("=")[0][-1]], int(line.split("=")[-1])
        )
        for line in fold_instructions
    ]

    return coord_array, fold_coord


def make_start_grid(coord_array):
    """
    This function generates a starting grid using the inputted starting
    coordinates
    """

    # generate the empty sheet of paper
    # in theory getting the max x and y values and using those to
    # generate the paper makes the most sense but I encountered
    # value errors this way for some reason
    # x_max = max(coord_array[:, 0]) + 1
    # y_max = max(coord_array[:, 1]) + 1

    paper = np.zeros((1400, 1400), np.int32)

    # populate the paper with the coordinates
    for x_pos, y_pos in coord_array:
        paper[y_pos, x_pos] += 1

    return paper


def fold_paper(paper, axis, position):
    """
    This function should fold an inputted paper grid along the axis
    chosen at a given position
    """
    if axis == 0:
        # top portion
        init_paper = paper[:position, :]
        # bottom portion
        flipped_paper = paper[position + 1:2 * position + 1, :]

    if axis == 1:
        # left portion
        init_paper = paper[:, :position]
        # right portion
        flipped_paper = paper[:, position + 1: 2 * position + 1]

    # fold the paper using np.flip
    folded_paper = init_paper | np.flip(flipped_paper, axis=axis)
    return folded_paper


def solve_part_1():
    coord_array, fold_coords = read_input("input.txt")
    paper = make_start_grid(coord_array)

    fold_axis = fold_coords[0][0]
    fold_pos = fold_coords[0][1]
    single_fold = fold_paper(paper, fold_axis, fold_pos)

    part_1_dots = single_fold.sum()

    print("part 1 solution:", part_1_dots)


def solve_part_2():
    coord_array, fold_coords = read_input("input.txt")
    paper = make_start_grid(coord_array)

    for fold_axis, fold_pos in fold_coords:
        paper = fold_paper(paper, fold_axis, fold_pos)

    plt.imshow(paper)
    plt.show()
    # print("part 1 solution:", part_1_dots)
