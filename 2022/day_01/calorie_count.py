# https://adventofcode.com/2022/day/1

import pandas as pd


class ElfCalories():
    """
    This class will contain dataframe that handles the calorie counts of
    the different elves
    """

    def __init__(self, file_name: str = "test.txt"):
        """
        This function reads in a text file that contains a list of integers and
        line breaks as a pandas series.

        Parameters
        ----------
        file_name: str
            The name of the file that we're going to read in

        """

        # read in the raw data including the line breaks
        with open(file_name, 'r') as f:
            raw_data = f.read()

        # split the data into individual elves where there are double line
        # breaks
        elf_split = raw_data.split('\n\n')

        # split each elf into calorie values
        cal_split = [elf.split('\n') for elf in elf_split]

        # convert to pd.DataFrame
        cal_df = pd.DataFrame(cal_split).fillna(0).astype('int').T

        self.cal_df = cal_df

    def find_top_cals(self, n: int = 3) -> int:
        """
        This function takes an input calorie dataframe and calculates
        the top n calories based on user input and then sums these together.

        Parameters
        ----------
        n: int
            The number of top calorie elves we want to sum over

        Returns
        -------
        max_cals: int
            The combined calorie count of the top n elves

        """

        # grab the calorie dataframe
        cal_df = self.cal_df

        # sum the columns and sort by descending
        summed_cals = cal_df.sum().sort_values(ascending=False)

        # filter to only the top elves
        top_cals = summed_cals[:n]

        # find the combined calories
        combined_cals = sum(top_cals)

        return combined_cals


def solution():
    pt1_sol = ElfCalories('input.txt').find_top_cals(n=1)
    pt2_sol = ElfCalories('input.txt').find_top_cals(n=3)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
