# https://adventofcode.com/2015/day/20

from collections import defaultdict


def calc_min_house(present_count=29000000, max_house=1e6, max_visits=False):
    """
    Determines the lowest house number that recieves the inputted
    number of presents.

    Each elf delivers presents to the house numbers that are multiples of their
    assigned number:

        The first Elf (number 1) delivers presents to every house
        The second Elf (number 2) delivers presents to every second house
        Elf number 3 delivers presents to every third house

    Each elf delivers 10 presents to the houses.
    We input an arbitrary upper limit of 1e6 for how many houses we
    think we need to loop through
    """
    # initialize the house dictionary that relates the house number and their
    # presents
    houses = defaultdict(int)

    # ensure the values are integers
    present_count = int(present_count)
    max_house = int(max_house)

    # brute force count the elves
    for elf in range(1, present_count):

        # depending if the elves stop after 50 houses or not we have
        # different present counts
        if max_visits:
            upper_bound = min(elf * 50 + 1, max_house)
            num_present = 11
        else:
            upper_bound = max_house
            num_present = 10

        # loop through the houses and get the present count
        for house in range(elf, upper_bound, elf):
            # add 10 times the elf number to the house present count
            houses[house] += elf * num_present

        # if we've found a house with the number of presents
        if houses[elf] >= present_count:
            # return elf count
            return elf


def sol_pipeline():
    """
    Quick command to generate the solutions
    """

    p1_sol = calc_min_house()
    print("P1 Solution:", p1_sol)

    p2_sol = calc_min_house(max_visits=True)
    print("P1 Solution:", p2_sol)
