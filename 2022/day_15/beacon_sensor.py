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

    def part1_sensor(self, row: int = 2000000) -> int:
        """
        Determines the number of positions that cannot contain a beacon based
        on the inputted beacon data and the inputted row.

        Parameters
        ----------
        row: int
            The row we're trying to check the positions that cannot contain
            a beacon
        """

        # load in the data
        beacon_data = self.beacon_data

        # keep track of occupied x values in the row
        occupied_pts = set()

        # create a list to keep track of intervals on the xaxis spanned
        x_intervals = []

        for line in beacon_data:
            sensor_x, sensor_y, beacon_x, beacon_y = line

            # calculate the distance between
            distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            # calculate the distance to the row
            to_row = distance - abs(sensor_y - row)

            # if the beacon doesn't intersect with the row then skip
            if to_row < 0:
                continue

            # calculate the area spanned
            lower_bound = sensor_x - to_row
            upper_bound = sensor_x + to_row

            # add the interval to the list of x intervals
            x_intervals.append((lower_bound, upper_bound))

            # if the beacon is on the row, add that point to the occupied pts
            if beacon_y == row:
                occupied_pts.add(beacon_x)

        # sort the values
        x_intervals.sort()

        # create a list of merged intervals
        merged_intervals = []

        # iterate over the x_intervals
        for lower_bound, upper_bound in x_intervals:
            # add current interval
            if not merged_intervals:
                merged_intervals.append([lower_bound, upper_bound])
                continue

            # Get the lower and upper bounds of the last interval in the
            # merged intervals list
            last_lower_bound, last_upper_bound = merged_intervals[-1]

            # If the current interval does not overlap the last interval,
            # add it to the merged intervals list
            if lower_bound > last_upper_bound + 1:
                merged_intervals.append([lower_bound, upper_bound])
                continue

            # Otherwise, merge the current interval with the last interval by
            # updating the upper bound of the last interval
            merged_intervals[-1][1] = max(last_upper_bound, upper_bound)

        # create a set to store the coordinates in the interval
        x_in_interval = set()

        # iterate over these intervals
        for lower_bound, upper_bound in merged_intervals:
            # add to the x_in_interval set
            for x in range(lower_bound, upper_bound + 1):
                x_in_interval.add(x)

        # calculate the difference
        unavailable = x_in_interval - occupied_pts

        # get the count
        unavailable_count = len(unavailable)

        return unavailable_count

    def part2_sensor(self, max_coord: int = 4000000) -> int:
        """
        Determines the distress frequency by calculating the position between
        0 < x or y < max_coord where the frequency = x * 4000000 + y

        Parameters
        ----------
        max_coord: int
            maximum value for the coordinates
        """

        # load in the data
        beacon_data = self.beacon_data

        # iterate over the rows from 0 to the maximum coordinate inclusive
        for row in range(max_coord + 1):

            # create a list to keep track of intervals on the xaxis spanned
            x_intervals = []

            # iterate over the beacons
            for line in beacon_data:
                sensor_x, sensor_y, beacon_x, beacon_y = line

                # calculate the distance between
                distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

                # calculate the distance to the row
                to_row = distance - abs(sensor_y - row)

                # if the beacon doesn't intersect with the row then skip
                if to_row < 0:
                    continue

                # calculate the area spanned
                lower_bound = sensor_x - to_row
                upper_bound = sensor_x + to_row

                # add the interval to the list of x intervals
                x_intervals.append((lower_bound, upper_bound))

            # sort the values
            x_intervals.sort()

            # create a list of merged intervals
            merged_intervals = []

            # iterate over the x_intervals
            for lower_bound, upper_bound in x_intervals:
                # add current interval
                if not merged_intervals:
                    merged_intervals.append([lower_bound, upper_bound])
                    continue

                # Get the lower and upper bounds of the last interval in the
                # merged intervals list
                last_lower_bound, last_upper_bound = merged_intervals[-1]

                # If the current interval does not overlap the last interval,
                # add it to the merged intervals list
                if lower_bound > last_upper_bound + 1:
                    merged_intervals.append([lower_bound, upper_bound])
                    continue

                # Otherwise, merge the current interval with the last interval
                # by updating the upper bound of the last interval
                merged_intervals[-1][1] = max(last_upper_bound, upper_bound)

            # Initialize the maximum x-coordinate within the merged intervals
            # to 0
            distress_x = 0
            # Iterate over the merged intervals
            for lower_bound, upper_bound in merged_intervals:
                # If the maximum x-coordinate is less than the lower bound of
                # the current interval, print x * 4000000 + Y and exit
                if distress_x < lower_bound:
                    distress_freq = distress_x * 4000000 + row
                    return distress_freq

                # Update the maximum x-coordinate to the maximum of max_x and
                distress_x = max(distress_x, upper_bound + 1)
                if distress_x > max_coord:
                    break


def solution():
    pt1_sol = Sensor('input.txt').part1_sensor()
    pt2_sol = Sensor('input.txt').part2_sensor()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

