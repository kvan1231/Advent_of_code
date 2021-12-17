# https://adventofcode.com/2021/day/6

import pandas as pd


class FishSpawn():
    """
    This class will contain the amount of time a fish
    needs until it spawns another fish

    Inputs
    ------
    input_name : string
        A comma separated file that denotes how much
        time until a fish spawns another
    """
    def __init__(self, input_name='test.txt'):
        """
        Reads in the data and creates a list counting it
        """

        fish_df = pd.read_csv(input_name, header=None)
        fish_counts = 9 * [0]

        for fish in fish_df.iloc[0, :]:
            fish_counts[fish] += 1
        self.fish_counts = fish_counts

    def iterate_days(self, num_days=18):
        """
        num_days : int
            The number of days to iterate to determine amount
            of fish
        """
        fish_counts = self.fish_counts
        
        # Update the counts as many times as there are days
        for day in range(num_days):

            # Move the first entry to the last spot and shift
            # entire list one over
            fish_counts = fish_counts[1:] + fish_counts[:1]

            # Add as many new fish to the list as there were
            # that just hit 0
            fish_counts[6] += fish_counts[8]

        # Sum the total number of fish
        print(sum(fish_counts))