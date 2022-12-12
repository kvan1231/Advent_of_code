# https://adventofcode.com/2022/day/8


import numpy as np


class Trees():
    """
    This class will contain the heights of the various trees in a numpy array
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the heights

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        raw_data = [list(tree.strip()) for tree in open(file_name)]

        # convert to numpy array
        tree_grid = np.array(raw_data, int)

        # save
        self.tree_grid = tree_grid

    def visible_tree_count(self) -> tuple:
        """
        This function will check if every tree to the right of the current
        tree are shorter than it, if it is then we denote that tree as visible.
        The function then rotates the whole grid 90 degrees and repeats the
        process. It also calculates the scenic score of a given tree by
        multiplying together the viewing distance from a given tree.
        """

        # load the grid
        tree_grid = self.tree_grid

        # create an empty grid to store which trees are visible
        visible_trees = np.zeros(tree_grid.shape, int)

        # create a grid of ones to calculate the scenic score
        scenic_grid = np.ones(tree_grid.shape, int)

        # # loop enough times to get all 4 directions
        for _ in range(4):
            # get the vertical and horizontal index
            for vert, hori in np.ndindex(tree_grid.shape):

                # check if all the trees to the right are lower
                lower_check = [
                    tree < tree_grid[vert, hori] for
                    tree in tree_grid[vert, hori+1:]
                ]

                # update the visible tree grid if all the trees are lower
                visible_trees[vert, hori] |= all(lower_check)

                # calculate the scenic value
                scenic_grid[vert, hori] *= next(
                    (
                        count + 1 for count, visible in enumerate(lower_check)
                        if ~visible
                    ), len(lower_check)
                )

            # spin
            tree_grid, visible_trees, scenic_grid = map(
                np.rot90, [tree_grid, visible_trees, scenic_grid]
            )

        # count how many trees are visible
        return (visible_trees.sum(), scenic_grid.max())


def solution():
    pt1_sol, pt2_sol = Trees('input.txt').visible_tree_count()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
