# https://adventofcode.com/2022/day/14

import re


class Sensor():
    """
    Contains the coordinates of the various sensors and their closest beacon
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the coordinates

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the dataS
        with open(file_name) as f:
            raw_data = f.read().splitlines()

        beacon_data = [
            tuple(map(int, re.findall(r"-?\d+", sensor))) for
            sensor in raw_data
        ]

        self.beacon_data = beacon_data