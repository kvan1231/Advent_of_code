# https://adventofcode.com/2015/day/3

from collections import defaultdict


def santa_walk(input_file='input.txt', robo_santa=False):
    """
    Read in a text file with directional input that tells us
    the movements of santa. Returns the total number of coordinates
    visited at least once
    """

    # initialize a dictionary
    houses = defaultdict(int)

    # read in the file
    with open(input_file, 'r') as f:
        directions = f.read()

    # initialize the first location
    x_pos, y_pos = 0, 0
    position = (x_pos, y_pos)

    # increment the first position to note we've visited
    houses[position] += 1

    # go through all the directional inputs and update the dictionary
    # if santa is going alone then enter this loop
    if not robo_santa:
        for move in directions:
            if move == '<':
                x_pos -= 1
            elif move == '>':
                x_pos += 1
            elif move == '^':
                y_pos += 1
            elif move == 'v':
                y_pos -= 1
            position = (x_pos, y_pos)
            houses[position] += 1
    # if we include robo santa then we split the directions
    # alternating between santa and robo santa
    if robo_santa:

        # create the x and y positions for robo and regular santa
        x1_pos, y1_pos = 0, 0
        x2_pos, y2_pos = 0, 0
        santa_move = directions[::2]
        robo_move = directions[1::2]

        # regular santas movements
        for move in santa_move:
            if move == '<':
                x1_pos -= 1
            elif move == '>':
                x1_pos += 1
            elif move == '^':
                y1_pos += 1
            elif move == 'v':
                y1_pos -= 1
            position = (x1_pos, y1_pos)
            houses[position] += 1

        # robo santas movements
        for move in robo_move:
            if move == '<':
                x2_pos -= 1
            elif move == '>':
                x2_pos += 1
            elif move == '^':
                y2_pos += 1
            elif move == 'v':
                y2_pos -= 1
            position = (x2_pos, y2_pos)
            houses[position] += 1

    # count the number of houses visited
    num_houses = len(houses.keys())
    return num_houses

