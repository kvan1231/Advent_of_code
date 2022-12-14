# https://adventofcode.com/2022/day/12

import numpy as np
import networkx as nx


class Grid():
    """
    Contains the heightmap of the surrounding area along with the starting
    point and end point
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the heightmap

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data as a numpy array
        raw_data = np.array(
            [list(height.strip()) for height in open(file_name)]
        )

        self.heightmap = raw_data

    def count_steps(self) -> tuple:
        """
        Finds the shortest path from the starting point to the end point
        going from a->z and returns the number of squares passed through
        """

        # initialize
        heightmap = self.heightmap

        # define the start and end points
        start_pt = list(zip(*np.where(heightmap == 'S')))[0]
        end_pt = list(zip(*np.where(heightmap == 'E')))[0]

        # replace the start and end points
        heightmap[start_pt] = 'a'
        heightmap[end_pt] = 'z'

        # create a networkx grid from the numpy array with the directional
        # graph
        grid = nx.grid_2d_graph(
            *heightmap.shape, create_using=nx.DiGraph
        )

        """
        we need to prevent the graph from taking steps that exceed one
        Character in distance on the alphabet. We can do this by grabbing
        the integer rep of a character with ord(). If the two characters
        are not sequential in the alphabet then the difference between
        the two ord() values will be greater than 1
        """
        grid.remove_edges_from(
            [
                (first, second) for first, second in grid.edges if
                ord(heightmap[second]) - ord(heightmap[first]) > 1
            ]
        )

        # with the large steps removed we can use networkx to find the
        # shortest path
        path = nx.shortest_path_length(grid, target=end_pt)
        step_count = path[start_pt]

        # luckily the shortest_path_length also calculates the shortest path
        # to a given point so we can just grab the minimum value that has
        # an index where the heightmap has the lowest height of 'a'
        all_step_counts = [
            path[a_ind] for a_ind in path if heightmap[a_ind] == 'a'
        ]
        fewest_moves = min(all_step_counts)

        return step_count, fewest_moves


def solution():
    pt1_sol, pt2_sol = Grid('input.txt').count_steps()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)