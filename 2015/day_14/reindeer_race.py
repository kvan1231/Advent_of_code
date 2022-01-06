# https://adventofcode.com/2015/day/14

from itertools import accumulate, cycle
from collections import defaultdict, Counter
import re


def read_data(input_file='test.txt'):
    """
    Read in the data and return it as a list
    """

    with open(input_file) as f:
        raw_data = f.read()

    # split it into a list
    data_list = [line for line in raw_data.split('\n')]

    return data_list


def gen_distances(input_list, n_secs=2504):
    """
    Takes an input_list that contains the different speeds and resting time
    of each reindeer. It then calculates the total distance covered after n
    seconds
    """

    # initialize the seating dictonary
    reindeer_dist = defaultdict(dict)

    for line in input_list:

        # we're using regex to pull the data
        temp_line = re.match(
            r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.',
            line
        )

        # pull reindeer, the speed, run time, and the rest time
        reindeer, speed, run_time, rest_time = temp_line.group(1, 2, 3, 4)

        timespan = cycle(
            [int(speed)] * int(run_time) + [0] * int(rest_time)
        )

        reindeer_dist[reindeer] = list(
            accumulate(next(timespan) for timestep in range(n_secs - 1))
        )

    # pull the farthest distance
    max_dist = max(dist[-1] for dist in reindeer_dist.values())

    # calculate the scores
    zip_pts = zip(*reindeer_dist.values())

    scores = [
        point for temp_dist in zip_pts for
        point, sub_dist in enumerate(temp_dist) if sub_dist == max(temp_dist)
    ]

    score_counts = Counter(scores)
    max_score = max(score_counts.values())

    return reindeer_dist, max_dist, max_score


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    test_data = read_data(input_file='test.txt')
    _, p1_test, p2_test = gen_distances(test_data, n_secs=1000)

    print("\nTests")
    print("=======")
    print("Part 1: ", p1_test)
    print("Part 2: ", p2_test)

    data = read_data("input.txt")
    _, p1_sol, p2_sol = gen_distances(data)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)
