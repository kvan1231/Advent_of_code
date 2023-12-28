""" https://adventofcode.com/2023/day/10 """

from collections import deque

class PipeMaze():
    """
    This class contains the map of the pipe maze which is represented by a
    collection of characters in a 2d grid where

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile,
    but your sketch doesn't show what shape the pipe has.
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file that contains the pipe layout

        Args:
            input_file (str, optional): Path to the text file containing
            the pipe data. Defaults to "input.txt".
        """

        # read in the data
        raw_grid = open(
            input_file, 'r', encoding='utf-8'
        ).read().strip().splitlines()

        # keep that data
        self.raw_grid = raw_grid

    def generate_pipe_path(self) -> set:
        """
        Takes in the raw grid and generates the pipe path in the
        form of a list

        Returns:
            set: a set containing the path of the pipe
        """

        raw_grid = self.raw_grid

        # lets find the starting point
        for row_ind, row in enumerate(raw_grid):
            for col_ind, character in enumerate(row):
                if character == "S":
                    start_row = row_ind
                    start_col = col_ind
                    break
            else:
                continue
            break

        # create the set
        pipe_path = {(start_row, start_col)}

        # create a deque for our pipe path to allow for appends and pops
        # from both sides of the list
        pipe_deque = deque([(start_row, start_col)])

        # while the pipe deque still has points in it
        while pipe_deque:
            temp_row, temp_col = pipe_deque.popleft()
            temp_char = raw_grid[temp_row][temp_col]

            # 
            if (
                temp_row > 0 and
                temp_char in "S|JL" and
                raw_grid[temp_row - 1][temp_char] in "|7F" and
                (temp_row - 1, temp_char) not in pipe_path
            ):
                pipe_path.add((temp_row - 1, temp_col))
                pipe_deque.append((temp_row - 1, temp_col))

        return pipe_path