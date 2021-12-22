# https://adventofcode.com/2021/day/22

import numpy as np


def sub_reactor_sim(input_file='test.txt'):
    """
    This function takes an input file that contains instructions that
    turns on and off various x, y, z coordinates for a reactor that
    spans -50 to 50 in x, y, and z directions.
    """

    # the x, y and z coordinates go from -50 to 50 so we're
    # going to make a grid that the same dimensions starting
    # from 0
    reactor_grid = np.zeros((101, 101, 101), dtype=np.int8)

    # open the input file
    instructions_list = open(input_file, 'r')

    # start looping through the lines
    for command in instructions_list:

        # split the lines
        sub_command = command.split(" ")

        # we're going to just brute force the dimensions
        reactor_ranges = [dim[2:] for dim in sub_command[1].split(',')]

        # shift the values to ensure no negative values
        x_start, x_end = [
            int(val) + 50 for val in reactor_ranges[0].split("..")
        ]
        y_start, y_end = [
            int(val) + 50 for val in reactor_ranges[1].split("..")
        ]
        z_start, z_end = [
            int(val) + 50 for val in reactor_ranges[2].split("..")
        ]

        # update the reactor grid based on ranges
        reactor_grid[
            x_start: x_end + 1, y_start: y_end + 1, z_start: z_end + 1
        ] = ['off', 'on'].index(sub_command[0])

    num_lit = reactor_grid.sum()

    return reactor_grid, num_lit


def total_reactor_sim(input_file='test.txt'):
    """
    This function takes an input file that contains instructions that
    turns on and off various x, y, z coordinates for a reactor that
    spans all of the reactors.
    """

    # create a list of reactors
    reactor_list = []

    # open the input file
    instructions_list = open(input_file, 'r')

    # start looping through the lines
    for command in instructions_list:

        # split the lines
        sub_command = command.split(" ")

        # we're going to just brute force the dimensions
        reactor_ranges = [dim[2:] for dim in sub_command[1].split(',')]

        # shift the values to ensure no negative values
        x_start, x_end = [
            int(val) for val in reactor_ranges[0].split("..")
        ]
        y_start, y_end = [
            int(val) for val in reactor_ranges[1].split("..")
        ]
        z_start, z_end = [
            int(val) for val in reactor_ranges[2].split("..")
        ]

        # we need to use the end points throughout so lets just
        # increment it now so we dont need to carry around the +1
        x_end += 1
        y_end += 1
        z_end += 1

        # determine if we're turning a reactor on or off
        reactor_state = ['off', 'on'].index(sub_command[0])

        # create a temp reactor containing all of the info
        temp_reactor = [
            x_start, x_end,
            y_start, y_end,
            z_start, z_end,
            reactor_state
        ]

        # create a temp list to store any new values
        new_reactor = []

        # loop through all of the sub reactors to see if they
        # interact with one another, start with a sub reactor
        for sub_reactor in reactor_list:

            # for intersection to occur we need the x, y and z
            # to overlap
            sub_x0 = sub_reactor[0]
            sub_x1 = sub_reactor[1]

            sub_y0 = sub_reactor[2]
            sub_y1 = sub_reactor[3]

            sub_z0 = sub_reactor[4]
            sub_z1 = sub_reactor[5]

            sub_state = sub_reactor[6]

            x_chk = x_end > sub_x0 and x_start < sub_x1
            y_chk = y_end > sub_y0 and y_start < sub_y1
            z_chk = z_end > sub_z0 and z_start < sub_z1

            # if all 3 dimensions overlap
            if x_chk and y_chk and z_chk:
                # now lets check which points overlap
                if sub_x0 < x_start:
                    # cut the left side off
                    new_sub = [
                        sub_x0, x_start,
                        sub_y0, sub_y1,
                        sub_z0, sub_z1,
                        sub_state
                    ]
                    # update the new start
                    sub_x0 = x_start
                    new_reactor.append(new_sub)
                if sub_x1 > x_end:
                    # cut the right side off
                    new_sub = [
                        x_end, sub_x1,
                        sub_y0, sub_y1,
                        sub_z0, sub_z1,
                        sub_state
                    ]
                    # update the new start
                    sub_x1 = x_end
                    new_reactor.append(new_sub)
                if sub_y0 < y_start:
                    # cut the top off
                    new_sub = [
                        sub_x0, sub_x1,
                        sub_y0, y_start,
                        sub_z0, sub_z1,
                        sub_state
                    ]
                    # update the new start
                    sub_y0 = y_start
                    new_reactor.append(new_sub)
                if sub_y1 > y_end:
                    # cut the bottom off
                    new_sub = [
                        sub_x0, sub_x1,
                        y_end, sub_y1,
                        sub_z0, sub_z1,
                        sub_state
                    ]
                    # update the new start
                    sub_y1 = y_end
                    new_reactor.append(new_sub)
                if sub_z0 < z_start:
                    # cut the front off
                    new_sub = [
                        sub_x0, sub_x1,
                        sub_y0, sub_y1,
                        sub_z0, z_start,
                        sub_state
                    ]
                    # update the new start
                    sub_z0 = z_start
                    new_reactor.append(new_sub)
                if sub_z1 > z_end:
                    # cut the back off
                    new_sub = [
                        sub_x0, sub_x1,
                        sub_y0, sub_y1,
                        z_end, sub_z1,
                        sub_state
                    ]
                    # update the new start
                    sub_z1 = z_end
                    new_reactor.append(new_sub)
            else:
                new_reactor.append(sub_reactor)

        # add the temp reactor
        new_reactor.append(temp_reactor)

        # update our reactor list
        reactor_list = new_reactor

    # convert to int64 numpy array
    reactor_array = np.array(reactor_list, dtype=np.int64)

    # find where the reactors are on
    on_inds = np.where(reactor_array[:, -1])

    # get only the ones that are on
    on_reactor = reactor_array[on_inds]

    dim_ranges = (
        (on_reactor[:, 1] - on_reactor[:, 0]) *
        (on_reactor[:, 3] - on_reactor[:, 2]) *
        (on_reactor[:, 5] - on_reactor[:, 4])
    )

    total_lights = dim_ranges.sum()

    return reactor_list, total_lights


print("Tests")
print("=====")

_, p1_test = sub_reactor_sim()
print("Part 1: ", p1_test)
_, p2_test = total_reactor_sim()
print("Part 2: ", p2_test)

print("\nResults")
print("=======")

_, p1_test = sub_reactor_sim("input.txt")
print("Part 1: ", p1_test)
_, p2_test = total_reactor_sim("input.txt")
print("Part 2: ", p2_test)
