""" https://adventofcode.com/2023/day/2 """

from collections import Counter
from functools import reduce
from operator import mul, or_

class Cube_Game():
    """
    Class containing the results of the cube game being played
    """
    def __init__(
            self,
            input_file: str = "input.txt",
            cube_max: dict = Counter({'red':12, 'green':13, 'blue':14})
        ) -> None:
        """
        This function reads in the text file containing the cube count in
        each cube game

        Args:
            input_file (str, optional): The text file containing the cube
            counts for each game and the game number. Defaults to "input.txt".

            cube_max (dict, optional): A dictionary containing the maximum
            number of each color cube that determines if a game is valid.
            Defaults to {'red':12, 'green':13, 'blue':14}.
        """

        # store the cube dict
        self.cube_max = cube_max

        # read in the data
        with open(input_file, 'r', encoding="utf-8") as f:
            raw_data = f.read()

        # split the data into invidual lines using \n
        split_data = raw_data.split('\n')
        
        # store the data
        self.cube_data = split_data

    def Game_Validate(self) -> tuple:
        """
        This function determines if the game is valid, if it is then
        it does the following: 
            takes the sum of the valid game ids and returns that value
            takes the sum of the product of the minimum cube counts and returns

        Returns:
            tuple: The sum of the game IDs that are valid games and the
            sum of the products
        """

        # load in data
        cube_max = self.cube_max
        cube_data = self.cube_data

        # initialize the output for the sum of valid game ids
        valid_games_sum = 0

        # initialize the output for the sum of the power of minimum cube counts
        valid_games_prod = 0

        # loop through the games
        for game in cube_data:

            # split the individual games by the colon
            game_str, cube_str = game.split(": ")

            # get the game id and convert to int
            game_id = int(game_str.split(" ")[1])

            # we need to split the game portion into cube counts
            cube_count = [
                [
                    cube.split(" ") for cube in round.split(", ")
                ] for round in cube_str.split("; ")
            ]

            # convert the counts into a dict
            cube_dict = [
                Counter(
                    {cube[1]:int(cube[0]) for cube in round}
                ) for round in cube_count
            ]

            # checks if the game is valid
            game_check = all(
                cube_draw <= cube_max for cube_draw in cube_dict
            )

            # if the game is valid then add the game id
            if game_check:
                valid_games_sum += game_id

            # we calculate the product even if the game isn't valid
            valid_games_prod += reduce(
                mul, reduce(
                    or_, cube_dict
                ).values()
            )

        return (valid_games_sum, valid_games_prod)

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol, pt2_sol = Cube_Game().Game_Validate()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
