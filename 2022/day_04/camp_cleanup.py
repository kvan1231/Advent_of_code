# https://adventofcode.com/2022/day/4

import numpy as np


class Sections():
    """
    This class will contain a list that reads in the sections each elf is
    assigned to clean
    """

    def __init__(self, file_name: str = "test.txt") -> list:
        """
        This function reads in the text file that contains the sections items

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split()

        # store it
        self.pairs = raw_data

    def solution(self, pt=1) -> int:
        """
        This function determines how many pairs have assignments where one
        overlaps the other depending on user input. If the user selects pt=1
        then we only increment when the overlap is complete, otherwise it
        counts on even partial overlaps

        Parameters
        ----------
        pt: int
            The part of the question from advent of code
                pt=1 count pairs with complete overlap
                pt=2 count pairs with partial overlap
        """

        # initialize
        pair_count = 0
        pairs = self.pairs

        # loop through the pairs
        for pair in pairs:

            # split the pair
            elf1, elf2 = pair.split(',')

            # split again into upper and lower values
            low1, up1 = map(int, elf1.split('-'))
            low2, up2 = map(int, elf2.split('-'))

            # generate numpy arrays from these values
            array1 = np.arange(low1, up1 + 1)
            array2 = np.arange(low2, up2 + 1)

            # if we're solving for part 1 then look for complete overlaps
            if pt == 1:
                if all(np.in1d(array1, array2)) or all(np.in1d(array2, array1)):
                    pair_count += 1

            # if we're solving for part 2 then look for partial overlaps
            elif pt == 2:
                if any(np.in1d(array1, array2)) or any(np.in1d(array2, array1)):
                    pair_count += 1

        return pair_count

    
def solution():
    pt1_sol = Sections('input.txt').solution(pt=1)
    pt2_sol = Sections('input.txt').solution(pt=2)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)