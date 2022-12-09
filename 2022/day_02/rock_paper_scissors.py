# https://adventofcode.com/2022/day/2

import pandas as pd


class RPS():
    """
    This class will contain a dataframe that reads in the rock paper scissors
    rounds
    """

    def __init__(self, file_name: str = "test.txt"):
        """
        This function reads in the text file that contains the rounds

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        raw_rounds = pd.read_csv(
            file_name, header=None,
            names=['opp', 'play'], delimiter=" ")

        self.rps_rounds = raw_rounds

    def part1_pts(self) -> int:
        """
        Returns the total points for part 1
        """
        raw_rounds = self.rps_rounds

        # replace the X, Y and Z with A, B and C
        rps_map = {
            'X': 'A',
            'Y': 'B',
            'Z': 'C'
        }
        rps_rounds = raw_rounds.replace({"play": rps_map})

        # calculate the shape points
        pt_map = {
            'A': 1,
            'B': 2,
            'C': 3
        }
        rps_rounds['shape_pts'] = rps_rounds['play'].map(pt_map)

        # calculate win/loss/draw points
        rps_rounds['wld_pts'] = rps_rounds.apply(win_loss, axis=1)

        total_pts = sum(rps_rounds['shape_pts']) + sum(rps_rounds['wld_pts'])
        return total_pts

    def part2_pts(self) -> int:
        """
        Returns the total points for part 2
        """
        rps_rounds = self.rps_rounds

        # calculate the win/loss/draw points
        shape_map = {
            'X': 0,
            'Y': 3,
            'Z': 6
        }
        rps_rounds['wld_pts'] = rps_rounds['play'].map(shape_map)

        # calculate the shape points
        rps_rounds['shape_pts'] = rps_rounds.apply(shape_gen, axis=1)

        total_pts = sum(rps_rounds['shape_pts']) + sum(rps_rounds['wld_pts'])
        return total_pts


def win_loss(df: pd.DataFrame) -> int:
    """
    Determines if a round of rock paper scissors ends up as a win, loss
    or draw and returns the points associated
    """

    if df['play'] == df['opp']:
        return 3
    # rock A > scissors C
    # scissors C > paper B
    # paper B > rock A
    elif (
        (df['play'] == 'A' and df['opp'] == 'C') or
        (df['play'] == 'C' and df['opp'] == 'B') or
        (df['play'] == 'B' and df['opp'] == 'A')
    ):
        return 6
    else:
        return 0


def shape_gen(df: pd.DataFrame) -> int:
    """
    Determines the shape the player used based on match result and opponent
    shape
    """

    # rock A > scissors C
    # scissors C > paper B
    # paper B > rock A
    win_map = {
        'A': 'B',
        'B': 'C',
        'C': 'A'
    }
    loss_map = {
        'A': 'C',
        'B': 'A',
        'C': 'B'
    }
    pt_map = {
        'A': 1,
        'B': 2,
        'C': 3
    }

    # lost
    if df['wld_pts'] == 0:
        return pt_map[loss_map[df['opp']]]
    # win
    elif df['wld_pts'] == 6:
        return pt_map[win_map[df['opp']]]
    # tie
    else:
        return pt_map[df['opp']]


def solution():
    pt1_sol = RPS('input.txt').part1_pts()
    pt2_sol = RPS('input.txt').part2_pts()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
