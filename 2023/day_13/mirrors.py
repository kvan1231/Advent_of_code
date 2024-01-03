""" https://adventofcode.com/2023/day/13 """

class Mirrors():
    """
    A class containing the information related to the
    mirrors and functions used to determine the reflection
    point in each
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file and extracts the raw data

        Args:
            input_file (str, optional): The text file containing the
            individual patterns where the reflection point needs to be
            found. Defaults to "input.txt".
        """

        # initialize
        grid_list = []

        # read in the data
        for block in open(input_file, 'r', encoding='utf-8').read().split("\n\n"):
            grid = block.splitlines()
            grid_list.append(grid)

        # keep the data
        self.grid_list = grid_list

    def find_mirror_point(self, grid:list, p2:bool = False) -> int:
        """
        A function that takes an inputted grid denoted by a list of strings and finds
        the reflection point in the grid

        Args:
            grid (list): A list of strings containing only '.' and '#' in a pattern
            p2 (boolean): A boolean controlling if we're going to look for a mirror
            point using the logic in part 1 or part 2. Default is False
                part 1 logic -
                    Mirror point is defined where the two sides of the grid of the
                    point are identical
                part 2 logic -
                    Mirror point is defined where the two sides of the grid differ
                    by one character swapping between '.' and '#'

        Returns:
            int: the index along the dimension where the grid is mirrored
        """

        # loop through the grid
        for mirror_ind in range(1, len(grid)):
            # prior to mirror point
            pre_grid = grid[:mirror_ind][::-1]

            # after mirror point
            post_grid = grid[mirror_ind:]

            # make sure the two subgrids have the same length
            pre_clean_grid = pre_grid[:len(post_grid)]
            post_clean_grid = post_grid[:len(pre_grid)]

            # if using part 2 logic, check if we only differ by 1 character
            if p2:
                if sum(
                    sum(
                        0 if a == b else 1 for a, b in zip(x, y)
                    ) for x, y in zip(pre_grid, post_grid)
                ) == 1:
                    return mirror_ind

            # using part 1 logic, check if the grids are identical then return the index
            else:
                if pre_clean_grid == post_clean_grid:
                    return mirror_ind

        # no index was found, return 0
        return 0

    def summarize_pattern(self, p2:bool = False) -> int:
        """
        Summarizes the pattern by taking the sum of the number of
        columns left of the mirror point and 100 * the number of rows
        above the horizontal mirror point

        Args:
            p2 (boolean): A boolean controlling if we're going to look for a mirror
            point using the logic in part 1 or part 2. Default is False
                part 1 logic -
                    Mirror point is defined where the two sides of the grid of the
                    point are identical
                part 2 logic -
                    Mirror point is defined where the two sides of the grid differ
                    by one character swapping between '.' and '#'

        Returns:
            int: the summarized value of the mirror points
        """

        # initialize
        summary_val = 0

        # grab the data
        grid_list = self.grid_list

        # loop through the grids
        for grid in grid_list:

            # try to find the mirror point in the rows
            mirror_row = self.find_mirror_point(grid, p2)
            summary_val += mirror_row * 100

            # try to find a mirror point in the columns
            # rotate the whole grid 90 degrees clockwise
            # https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
            rot_grid = list(zip(*grid))
            mirror_col = self.find_mirror_point(rot_grid, p2)

            summary_val += mirror_col

        return summary_val

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Mirrors().summarize_pattern()
    pt2_sol = Mirrors().summarize_pattern(p2=True)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
