""" https://adventofcode.com/2023/day/6 """

import math

class BoatRace():
    """
    Class containing the information and outputs for the boat race
    """
    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Takes the input text file that contains the times and distances for
        the various boat races

        Args:
            input_file (str, optional): A text file containing the time and
            distances for each individual boat race. Each column represents a
            different race. Defaults to "input.txt".
        """

        # read in the raw data
        raw_times, raw_dists = open(input_file).read().split('\n')

        # clean the data up and convert to ints
        time_vals = list(map(int,raw_times.split(":")[1].split()))
        dist_vals = list(map(int,raw_dists.split(":")[1].split()))

        # store the data
        self.time_vals = time_vals
        self.dist_vals = dist_vals

    def simulate_races(self, p1:bool = True) -> int:
        """
        Simulates the races based on the time and distance data and
        determines the different ways a racer can beat the record for
        a given race denoted by a column. We then take the product of
        these values and return it.

        Args:
            p1 (boolean, optional): A boolean to determine if this function
            calculates part 1 if p1=True of the problem where we loop through
            all of the races or part 2 where we combine the times and distances
            into one value if p1=False.

        Returns:
            int: product of the number of ways a boat can beat the record
        """

        # load in the data
        time_data = self.time_vals
        dist_data = self.dist_vals

        # if part 1, just take the values as a list
        if p1:
            time_vals = time_data
            dist_vals = dist_data

        # if part 2, combine the values into one
        else:
            time_vals = [int(
                ''.join(list(map(str, time_data)))
            )]
            dist_vals = [int(
                ''.join(list(map(str, dist_data)))
            )]

        # generate a list of ways to win
        # win_list = [1] * len(time_vals)

        # I decided not to use a list to carry the possible win
        # combinations since this could lead to a large number of
        # values being stored for no reason since we're only
        # interested in the product of all of these values.

        # initialize the output
        win_prod = 1

        # loop through races
        for race_ind in range(len(time_vals)):

            time = time_vals[race_ind]
            dist = dist_vals[race_ind]

            # initialize number of wins
            wins = 0

            # get all possible hold times
            for hold_time in range(time):

                # see if we can beat the distance
                if hold_time * (time - hold_time) > dist:
                    wins += 1

            # change it in the win list
            # win_list[race_ind] = wins
            win_prod *= wins

        # return the product of the possible wins
        return win_prod

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = BoatRace('input.txt').simulate_races(p1=True)
    pt2_sol = BoatRace('input.txt').simulate_races(p1=False)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
