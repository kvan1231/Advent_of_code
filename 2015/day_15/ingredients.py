# https://adventofcode.com/2015/day/15

import re
import numpy as np


def read_data(input_file='test.txt'):
    """
    Read in the data and return it as a list
    """

    with open(input_file) as f:
        raw_data = f.read()

    # split it into a list
    data_list = [line for line in raw_data.split('\n')]

    return data_list


def ingredients(input_list):
    """
    We need to calculate the ingredient combination that results
    in the most points. The points are calculated with 100 combined
    ingredients as

        pts = cap_pts * dur_pts * fla_pts * tex_pts
        cat_pts = sum(cat_val_i * num_i + cat_val_j + num_j + ...)
            where each category (cat) is given a weight

        100 = sum(num)
            the sum of all ingredients equals to 100
    """
    # initialize the ingredient list
    ingredient_list = []

    for line in input_list:

        # we're using regex to pull the data
        cap, dur, fla, tex, cal = map(
            int, re.findall(r'-?\d+', line)
        )
        ingredient_list.append([cap, dur, fla, tex, cal])

    ing_array = np.array(ingredient_list)
    # initialize the scores

    max_score = 0
    max_cal_score = 0

    # there should be a recursive or smarter way to do this but
    # I coulnd't think of it so here is a triple nested loop instead
    # because we only have 4 properties in our ingredients.
    for ind1 in range(0, 101):
        # print(ind1)
        for ind2 in range(0, 101 - ind1):
            # print(ind2)
            for ind3 in range(0, 101 - ind1 - ind2):
                # print(ind3)
                ind4 = 100 - ind1 - ind2 - ind3
                # print(ind4)

                # create an array of the counts for easier multiplication
                ind_array = np.array([
                    ind1, ind2, ind3, ind4, 1
                ])

                # multiply the properties by the counts
                pt_array = sum((ing_array.T * ind_array[:len(ing_array)]).T)

                if any(pt_array <= 0):
                    cur_score = 0
                else:
                    cur_score = np.prod(pt_array[:-1], dtype=np.int64)

                    # replace any scores with new maximums
                    max_score = max(cur_score, max_score)
                    if pt_array[-1] == 500:
                        max_cal_score = max(max_cal_score, cur_score)

    return max_score, max_cal_score


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    test_data = read_data(input_file='test.txt')
    p1_test, p2_test = ingredients(test_data)

    print("\nTests")
    print("=======")
    print("Part 1: ", p1_test)
    print("Part 2: ", p2_test)

    data = read_data("input.txt")
    p1_sol, p2_sol = ingredients(data)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
