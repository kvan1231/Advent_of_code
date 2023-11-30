# https://adventofcode.com/2022/day/19

import re
import numpy as np


class Blueprint:
    """
    Contains the blueprints relating the costs to each robot
    """
    def __init__(self, file_name: str = 'test.txt') -> None:
        """
        Reads in the text file that contains the cost affiliated with each
        robot and stores is

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        raw_data = []

        with open(file_name) as f:
            for _, full_line in enumerate(f.readlines()):
                line = full_line.strip()

                # extract the integers from the line
                blueprint_map = map(
                    int, re.findall(r'\d+', line)
                )

                # convert it to a list of integers
                bp_vals = list(blueprint_map)

                # split the data into tuples

                # blueprint number
                bp_num = bp_vals[0]

                # we're going to split all of the data into numpy arrays
                # containing the cost and production of each robot. The order
                # of the indices are: ore, clay, obsidian and geodes.

                # ore
                ore_cost = np.array([bp_vals[1], 0, 0, 0])
                ore_prod = np.array([1, 0, 0, 0])

                # clay
                cly_cost = np.array([bp_vals[2], 0, 0, 0])
                cly_prod = np.array([0, 1, 0, 0])

                # obsidian
                obs_cost = np.array([bp_vals[3], bp_vals[4], 0, 0])
                obs_prod = np.array([0, 0, 1, 0])

                # geodes
                geo_cost = np.array([bp_vals[5], 0, bp_vals[6], 0])
                geo_prod = np.array([0, 0, 0, 1])

                # no robot
                nul_cost = np.array([0, 0, 0, 0])
                nul_prod = np.array([0, 0, 0, 0])

                blueprint_vals = (bp_num,
                                  (ore_cost, ore_prod),
                                  (cly_cost, cly_prod),
                                  (obs_cost, obs_prod),
                                  (geo_cost, geo_prod),
                                  (nul_cost, nul_prod))

                raw_data.append(blueprint_vals)

        self.raw_data = raw_data

    def part1(self):
        efficiency = 0
        for bp_num, *blueprint in self.raw_data:
            print(blueprint)
            efficiency += self._calc_quality(blueprint) * bp_num

        return efficiency

    def _calc_quality(self, blueprint, minutes: int = 24):
        """
        Calculates the quality of a blueprint
        """

        # start with an intial state
        bag_state = [(np.array([0, 0, 0, 0]),
                     np.array([1, 0, 0, 0]))]

        # loop through the steps
        for step in range(minutes, 0, -1):
            print(step)
            bp_step = list()

            # track current resources and robots available
            for resources, robots in bag_state:

                # determine cost and output of each blueprint
                for cost, prod in blueprint:

                    # if we can create that robot, do so
                    if all(cost <= resources):
                        bp_step.append((
                            resources + robots - cost, prod + robots
                        ))

            bag_state = self._prune(bp_step)
        return max(resources[0] for resources, _ in bag_state)

    # key and prune taken from a solution here
    # https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
    def _key(self, a):
        return tuple(a[0]+a[1]) + tuple(a[1])

    def _prune(self, x):
        unique_values = {self._key(x): x for x in x}.values()
        sorted_values = sorted(unique_values, key=self._key)
        return sorted_values
