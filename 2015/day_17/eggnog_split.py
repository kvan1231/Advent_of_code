# https://adventofcode.com/2015/day/17

from itertools import combinations


def read_data(input_file='input.txt'):
    """
    Read in the data and return it as a list
    """

    # open the file
    with open(input_file) as f:
        # read the file as a list
        str_list = f.read().splitlines()

    # convert that list of strings to ints
    bottle_list = list(map(int, str_list))

    # return that list
    return bottle_list


def bottle_combinations(bottle_list, tot_sum):
    """
    Takes a list of bottles that we will calculate the combination
    of that results in the total sum of interst
    """

    # intialize the possible combinations
    total_combs = 0
    subtotal_combs = 0

    # loop through all possible bottle combinations
    for bottle_ind in range(len(bottle_list)):
        for permuation in combinations(bottle_list, bottle_ind):

            # if the sum of the various bottles equals to the sum
            if sum(permuation) == tot_sum:

                # iterate the possible combinations
                total_combs += 1

        if total_combs and not subtotal_combs:
            # get the minimum number
            subtotal_combs = total_combs

    # return the combinations
    return total_combs, subtotal_combs
