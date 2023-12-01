""" https://adventofcode.com/2023/day/1 """

import re

class Calibration():
    """
    Class representing the calibration document
    """
    def __init__(self, input_file: str ="input.txt") -> None:
        """
        This function reads in the text file containing the calibration along
        with initializing required data

        Args:
            input_file (str, optional): The path to the text file containing
            the calibration data. Defaults to "input.txt".
        """

        # read in the data
        with open(input_file, 'r', encoding="utf-8") as f:
            raw_data = f.read()

        # split the data into invidual lines using \n
        split_data = raw_data.split('\n')

        # store the data
        self.calibration_data = split_data

        # generate a list of all of the digits used later
        digits = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine"
        ]

        self.digits = digits

    def word_to_num(self, string:str) -> str:
        """
        This function takes in a string and either returns the number
        equivalent of that string or returns that value as is

        Args:
            string (str): The input string to try and match to a number

        Returns:
            str: The appropriate number output
        """

        digits = self.digits

        if string in digits:
            return str(digits.index(string) + 1)
        return string


    def calibrated_sum(self, p1=True) -> int:
        """
        This function strips off the integers in each row of calibration
        data to generate a number from the first and last integers found. 
        The function then sums up all of these integers and returns this sum

        Args:
            p1 (bool, optional): True if we're looking for the part 1 solution,
            false if we're looking for the part 2 solution. Defaults to True.

        Returns:
            int: The sum of the integers from the calibration data set
        """

        # read in the data
        cali_data = self.calibration_data

        # grab the digits
        digits = self.digits

        # intialize a list to contain the ints
        cali_ints = []

        # create a regex string thing for finding digits
        digit_regex = "(?=(" + "|".join(digits) + "|\\d))"

        # loop through the rows
        for cali_row in cali_data:
            # part 1 simple grabbing of integer values
            if p1:
                tmp_int = ''.join(filter(str.isdigit, cali_row))
            # part 2 we need to map words to integers
            else:
                tmp_int = [
                    *map(self.word_to_num, re.findall(digit_regex, cali_row))
                    ]

            # grab the first and last integer
            cali_int = tmp_int[0] + tmp_int[-1]

            # append this new 2 digit integer
            cali_ints.append(int(cali_int))

        return sum(cali_ints)

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Calibration().calibrated_sum()
    pt2_sol = Calibration().calibrated_sum(p1=False)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
