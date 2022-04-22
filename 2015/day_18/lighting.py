# https://adventofcode.com/2015/day/18

import numpy as np
import scipy.ndimage as ndimage


def read_data(input_file='input.txt'):
    """
    Reads in an input file and outputs a grid that
    represents the lights
    """

    # read in the raw data
    with open(input_file) as f:
        raw_data = f.read()

    # convert the data into a grid
    raw_grid = raw_data.split()
    # determine the rows and columns
    rows = len(raw_grid)
    cols = len(raw_grid[0])

    # initialize the grid that is 100x100 booleans
    light_grid = np.zeros((rows, cols), dtype=bool)

    # loop through the input file to turn lights on
    for row, column in enumerate(raw_grid):
        light_grid[row][[i for i, chr in enumerate(column) if chr == '#']] = 1

    return light_grid


def iterate_lights(light_grid, iterations=4, corner_active=False):
    """
    Evolves the grid to turn on and off lights depending on neighbours
    """

    grid = light_grid

    # determine the number of rows and columns in the grid, convert to index
    rows = len(grid) - 1
    cols = len(grid[0]) - 1

    # if this is part 2 of the question then the grid corners are always active
    if corner_active:
        grid[0, 0] = 1
        grid[0, cols] = 1
        grid[rows, 0] = 1
        grid[rows, cols] = 1

    # iterate through the grid
    for iteration in range(iterations):
        # iterate the grid light
        grid = ndimage.generic_filter(
            grid,
            lambda x: sum(x) - 1 in [2, 3] if x[4] else sum(x) == 3,
            size=(3, 3),
            mode='constant'
            )
        # if part 2 then actviate the corners
        if corner_active:
            grid[0, 0] = 1
            grid[0, cols] = 1
            grid[rows, 0] = 1
            grid[rows, cols] = 1

    # return the grid
    return grid


def sol_pipeline():
    """
    Output the solutions
    """
    light_grid = read_data()

    p1_sol = iterate_lights(
        light_grid,
        iterations=100
    ).sum()
    p2_sol = iterate_lights(
        light_grid,
        iterations=100,
        corner_active=True
    ).sum()

    print("P1 sol:", p1_sol)
    print("P2 sol:", p2_sol)
