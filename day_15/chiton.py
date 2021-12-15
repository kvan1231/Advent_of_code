# https://adventofcode.com/2021/day/15

"""
This is a path finding problem so we should be able to
solve this using dijkstras algorithm
"""

import numpy as np

# fun fact, queue.PriorityQueue is effectively a wrapper on heapq
# https://stackoverflow.com/questions/36991716/whats-the-difference-between-heapq-and-priorityqueue-in-python/36991722#36991722
import heapq


def dijkstra(input_file='test.txt', scale=1):
    """
    Trying to solve this problem using dijkstra

    Inputs
    ------
    input_file : string
        the path to the file containing the map
    scale : integer
        1 or 5 depending if we want to solve part 1
        or part 2 where the map is scaled 5 times
    """

    # read in the file
    path_map = np.genfromtxt(
        input_file, delimiter=1, dtype=np.int32
    )

    # generate the direction of all of the neighbours
    neighbour_shift = [
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1]
    ]

    # get the shape of the map
    y_len, x_len = path_map.shape

    # create an array of zeros to store the cost of the distance
    # up until that point
    cost_map = np.zeros((y_len * scale, x_len * scale), dtype=np.int32)

    heap = [(0, 0, 0)]
    while heap:
        (distance, y_pos, x_pos) = heapq.heappop(heap)
        # print(distance, y_pos, x_pos)
        # make sure we stay within the map
        row_check = (y_pos < 0 or y_pos >= y_len * scale)
        col_check = (x_pos < 0 or x_pos >= x_len * scale)
        if row_check or col_check:
            continue

        # calculate the cost to the current location
        scaled_y_pos = y_pos % y_len
        scaled_x_pos = x_pos % x_len
        curr_loc = path_map[scaled_y_pos, scaled_x_pos]

        # the additional cost associated in the scaled maps
        scaled_cost = y_pos // y_len + x_pos // x_len

        partial_cost = curr_loc + scaled_cost

        # wrap the value around 9 -> 1
        while partial_cost > 9:
            partial_cost -= 9

        # calculate the total cost of the positon including the distance
        cost = partial_cost + distance

        # update the cost in the empty map
        if cost_map[y_pos, x_pos] == 0 or cost < cost_map[y_pos, x_pos]:
            cost_map[y_pos, x_pos] = cost
        else:
            continue

        # if we've reached the end
        y_end = (y_pos == y_len * scale - 1)
        x_end = (x_pos == x_len * scale - 1)
        if y_end and x_end:
            # print(cost)
            break

        # move to a neighbour
        for sub_shift in neighbour_shift:
            neigh_y = y_pos + sub_shift[0]
            neigh_x = x_pos + sub_shift[1]

            heapq.heappush(
                heap, (cost_map[y_pos, x_pos], neigh_y, neigh_x)
            )

    # get the initial cost, final cost and difference
    init_cost = cost_map[0, 0]
    final_cost = cost_map[-1, -1]
    return final_cost - init_cost


p1_cost = dijkstra(input_file='input.txt')
print("part 1 solution:", p1_cost)

p2_cost = dijkstra(input_file='input.txt', scale=5)
print("part 2 solution:", p2_cost)
