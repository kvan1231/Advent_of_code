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

        # keep that data
        self.raw_grid = raw_grid
        self.pipe_path = pipe_path
        self.pipe_deque = pipe_deque

    def generate_pipe_path(self) -> set:
        """
        Takes in the raw grid and generates the pipe path in the
        form of a list and returns it. It also generates a clean grid
        and returns that as well

        Returns:
            set: a set containing the path of the pipe
        """

        # load in the data
        grid = self.raw_grid
        pipe_path = self.pipe_path
        pipe_deque = self.pipe_deque

        # set of possible pipes to swap out with S
        poss_pipes = {
            "|", "-", "J", "L", "7", "F"
        }

        # loop through the positions
        while pipe_deque:

            # get the positions
            row, col = pipe_deque.popleft()
            char = grid[row][col]

            # check up
            if (
                row > 0 and
                char in "S|JL" and
                grid[row - 1][col] in "|7F" and
                (row - 1, col) not in pipe_path
            ):
                pipe_path.add((row - 1, col))
                pipe_deque.append((row - 1, col))
                if char == "S":
                    poss_pipes &= {"|", "J", "L"}

            # check down
            if (
                row < len(grid) - 1 and
                char in "S|7F" and
                grid[row + 1][col] in "|JL" and
                (row + 1, col) not in pipe_path
            ):
                pipe_path.add((row + 1, col))
                pipe_deque.append((row + 1, col))
                if char == "S":
                    poss_pipes &= {"|", "7", "F"}

            # check left
            if (
                col > 0 and
                char in "S-J7" and
                grid[row][col - 1] in "-LF" and
                (row, col - 1) not in pipe_path
            ):
                pipe_path.add((row, col - 1))
                pipe_deque.append((row, col - 1))
                if char == "S":
                    poss_pipes &= {"-", "J", "7"}

            # check right
            if (
                col < len(grid[row]) - 1 and
                char in "S-LF" and
                grid[row][col + 1] in "-J7" and
                (row, col + 1) not in pipe_path
            ):
                pipe_path.add((row, col + 1))
                pipe_deque.append((row, col + 1))
                if char == "S":
                    poss_pipes &= {"-", "L", "F"}

        assert len(poss_pipes) == 1
        (start_sym, ) = poss_pipes

        # update the grid to replace the S with new starting symbol
        updated_grid = [
            row.replace("S", start_sym) for row in grid
        ]

        # clean the grid to remove the junk pipes
        clean_grid = [
            "".join(
                char if (row_ind, col_ind) in pipe_path
                else "." for col_ind, char in enumerate(row)
            ) for row_ind, row in enumerate(updated_grid)
        ]

        return pipe_path, clean_grid

    def furthest_position(self) -> int:
        """
        Calculates the distances to the furthest position from the starting
        point

        Returns:
            int: distance to the furthest point
        """

        pipe_path, _= self.generate_pipe_path()

        return len(pipe_path) // 2

    def find_enclosed(self) -> int:
        """
        Calculates the area enclosed within the pipes

        Returns:
            int: The total enclosed area
        """

        pipe_path, grid = self.generate_pipe_path()

        # define a set for outside the loop
        outside_section = set()

        # loop through the values to see if we're inside
        for r_ind, row in enumerate(grid):
            inside = False
            up = None
            for c_ind, char in enumerate(row):
                if char == "|":
                    assert up is None
                    inside = not inside
                elif char == "-":
                    assert up is not None
                elif char in "LF":
                    assert up is None
                    up = char == "L"
                elif char in "7J":
                    assert up is not None
                    if char != ("J" if up else "7"):
                        inside = not inside
                    up = None
                elif char == ".":
                    pass
                else:
                    raise RuntimeError(
                        f"unexpected character (horizontal): {char}"
                        )
                if not inside:
                    outside_section.add((r_ind, c_ind))

        return(len(grid) * len(grid[0]) - len(outside_section | pipe_path))

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = PipeMaze().furthest_position()
    pt2_sol = PipeMaze().find_enclosed()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
