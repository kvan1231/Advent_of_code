# https://adventofcode.com/2022/day/18

import networkx as nx


class LavaDroplets:
    """
    Contains the x, y, z positions of the laval droplets read in from a text
    file
    """
    def __init__(self, file_name: str = 'test.txt') -> None:
        """
        This function reads in the text file that contains the positions of
        each lava droplet

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        with open(file_name) as f:
            droplet_positions = [
                tuple(int(pos) for pos in drop.strip().split(","))
                for drop in f.readlines()
            ]

        # store that information
        self.droplet_positions = droplet_positions

    def surface_sim(self, p1=True) -> int:
        """
        Takes the positions of the lava droplets and determines the number of
        sides not connected to another droplet

        Parameters
        ----------
        p1: boolean
            A boolean controlling whether or not we're interested in part 1
            or part 2 of the question. Set to true if we're doing part 1 and
            false if we're doing part 2
        """

        # initialize
        droplet_positions = self.droplet_positions

        # flatten the positions
        dims = list(sum(droplet_positions, ()))

        min_pos = min(dims) - 2
        max_pos = max(dims) + 2

        # create a grid graph that spans our entire range with some buffer
        entire_range = nx.grid_graph(
            dim=[range(min_pos, max_pos)] * 3
        )

        # if we're only doing part 1 then the relevant volume we're calculating
        # the surface of is just the droplet positons
        if p1:
            relevant_volume = droplet_positions
        else:
            # create a new range to handle air pockets
            air_pockets = entire_range.copy()

            # remove the lava drops from the air pockets
            air_pockets.remove_nodes_from(droplet_positions)

            # find the connecting air pockets
            connected_air = nx.node_connected_component(
                air_pockets, (-1, -1, -1)
            )

            relevant_volume = connected_air

        unique_sides = sum(
            1 for _ in nx.edge_boundary(entire_range, relevant_volume)
        )

        return unique_sides
