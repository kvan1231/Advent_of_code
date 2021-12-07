# https://adventofcode.com/2021/day/7

import pandas as pd


class CrabSubmarine():
    """
    This class will contain the horizontal positions
    of the crab submarines

    Inputs
    ------
    input_name : string
        A comma separated file the locations of the crabs
    """
    def __init__(self, input_name='test.txt'):
        """
        Reads in the data
        """

        crab_df = pd.read_csv(input_name, header=None)
        self.crab_df = crab_df.T

    def cheapest_outcome(self):
        """
        Determines the cheapest possible outcome where
        each crab must move to a common position. The
        cost of the outcome is the absolute sum of the
        difference between the starting point and the
        end position. Mathematically we're minimizing
        the L1 norm of the distances.
        """

        init_pos_df = self.crab_df

        # The median value minimizes the L1 norm of the distances
        median_pos = init_pos_df.median()

        # calculate the absolute difference between the init and median
        pos_diff = abs(init_pos_df - median_pos)

        # return the sum of the position differences
        tot_cost = int(pos_diff.sum())
        print(tot_cost)

    def scaling_cheap_outcome(self):
        """
        Determines the cheapest possible outcome similar to
        the 'cheapest_outcome' function above except the cost
        of each move increases per move of the crab. This means
        that the median value is no longer the cheapest position.
        Due to the cost of the movement changing for N to
        N * (N+1) we can assume that the cheapest position is
        somewhere between the L1 and L2 norm. The L2 norm is the
        sum of the squared vector values or N^2.
        """

        init_pos_df = self.crab_df

        # Find the integer mean value
        mean_pos = int(init_pos_df.mean())

        # calculate the absolute difference between the init and mean
        pos_diff_grow = self.cost(abs(init_pos_df - mean_pos))

        # return the sum of the position differences
        tot_cost_grow = int(pos_diff_grow.sum())

        min_crab = init_pos_df.values.min()
        max_crab = init_pos_df.values.max()

        # Check other values to be sure
        for midpoint in range(min_crab, max_crab+1):
            temp_diff = self.cost(abs(init_pos_df - midpoint))
            temp_tot = int(temp_diff.sum())
            tot_cost_grow = min(
                tot_cost_grow, temp_tot
            )
        print(tot_cost_grow)

    def cost(self, move):
        """
        A function that calculates the total cost
        of moving n number of steps using the equation

        move = ( move + 1 ) // 2
        """

        return move * (move + 1) // 2