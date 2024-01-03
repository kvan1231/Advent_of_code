""" https://adventofcode.com/2023/day/11 """

class Galaxy():
    """
    This class contains the map denoting where the galaxies are
    in relation to each other
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file that contains the galaxy map

        Args:
            input_file (str, optional): the path to the text file containing
            the galaxy data. Defaults to "input.txt".
        """

        # read in the data
        galaxy_map = open(
            input_file, 'r', encoding='utf-8').read().splitlines()

        # store the data
        self.galaxy_map = galaxy_map

    def calculate_distance(self, expansion:int = 2) -> int:
        """
        Takes the galaxy map and calculates the sum of the total distances between
        all possible pairs of galaxies

        Args:
            expansion (int, optional): the amount of expansion for each empty row or
            column in the galaxy data. Defaults to 2.

        Returns:
            int: The total distance
        """

        # initialize the total distance
        total_distance = 0

        # get the galaxy map
        galaxy_map = self.galaxy_map

        # find the empty rows and columns
        empty_row = [
            r_ind for r_ind, row in enumerate(galaxy_map)
            if all (character == "." for character in row)
        ]
        empty_col = [
            c_ind for c_ind, col in enumerate(zip(*galaxy_map))
            if all (character == "." for character in col)
        ]

        # find the galaxies
        galaxies = [
            (r_ind, c_ind) for r_ind, row in enumerate(galaxy_map)
            for c_ind, character in enumerate(row) if character == "#"
        ]

        # loop through the galaxies and their index
        for index, (init_row, init_col) in enumerate(galaxies):
            # for all other galaxies to generate pairs
            for (fin_row, fin_col) in galaxies[:index]:

                # grab the ends of the rows/cols
                min_row = min(init_row, fin_row)
                max_row = max(init_row, fin_row)

                min_col = min(init_col, fin_col)
                max_col = max(init_col, fin_col)

                # loop through the row and column values and add
                # 1 if it isn't an empty row, and add the expansion
                # value instead if it is empty
                for row in range(min_row, max_row):
                    if row in empty_row:
                        total_distance += expansion
                    else:
                        total_distance += 1

                for col in range(min_col, max_col):
                    if col in empty_col:
                        total_distance += expansion
                    else:
                        total_distance += 1

        return int(total_distance)

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Galaxy().calculate_distance(expansion=2)
    pt2_sol = Galaxy().calculate_distance(expansion=int(1e6))

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
