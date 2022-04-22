# https://adventofcode.com/2015/day/16

from collections import defaultdict


def read_data(input_file="input.txt"):
    """
    Read in the data and return it as a dictionary
    """

    sue_dict = defaultdict(dict)

    for line in open(input_file):
        # split the lines
        line = line.split()
        # the sue number is the second item in the list
        sue_num = int(line[1].strip(':'))
        # all the properties related to sue are the following items
        sue_props = line[2:]

        # loop through the items in the line
        for prop_ind in range(len(sue_props) // 2):
            # strip the strings of extra punctuation
            item = sue_props[2*prop_ind].strip(':')
            num = sue_props[2*prop_ind + 1].strip(',')

            # add to the dictionary
            sue_dict[sue_num][item] = int(num)

    # return the dictionary
    return sue_dict


def aunt_props(prop_file='aunt_props.txt'):
    """
    Reads in a given text file and uses it to generate a dictionary
    """
    # initialize an empty dictionary
    props = {}

    # open the file and read the lines
    for line in open(prop_file):
        # split and strip the lines
        line = line.strip().split()
        # the first item in the line is the item name
        item = line[0].strip(":")
        # the second item in the line is the number
        num = int(line[1])

        # add this key-attribute pair to the dictionary
        props[item] = num

    return props


def match_sue(sue_dict, key_props):
    """
    Finds the aunt sue that matches with the given properties input
    """

    # loop through the various aunts
    for sue_int in sue_dict:

        # grab the appropriate row
        sue = sue_dict[sue_int]

        # check if the numbers of the items match for part 1
        p1_chk = all(
            item in key_props.items() for item in sue.items()
        )

        # if they do then we have the solution to p1
        if p1_chk:
            print("part 1 sol:", sue_int)
            p1_sue = sue_int

        # start with our check being true
        p2_chk = True

        # check if the numbers invalidate our p2 check
        for item in sue:
            # if the sue property isn't in key properties
            if item not in key_props:
                p2_chk = False
            # if the number of cats or trees is less than
            if item in ["cats", "trees"]:
                if sue[item] <= key_props[item]:
                    p2_chk = False
            # if the number of pomeranians or goldfish is greater than
            elif item in ["pomeranians", "goldfish"]:
                if sue[item] >= key_props[item]:
                    p2_chk = False
            # if any of the numbers just dont match
            elif sue[item] != key_props[item]:
                p2_chk = False

        if p2_chk:
            print("part 2 sol:", sue_int)
            p2_sue = sue_int

    return p1_sue, p2_sue
