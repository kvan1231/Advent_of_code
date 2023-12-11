""" https://adventofcode.com/2023/day/8 """

from math import gcd

class Map():
    """
    The class containing the map information that includes the map
    network and the sequence of left/right used to navigate
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input text file that contains the navigation sequence
        and the map network

        Args:
            input_file (str, optional): the path to the text file
            containing the map information. Defaults to "input.txt".
        """

        # read in the data
        navigation, _, *nodes = open(
            input_file, 'r', encoding="utf-8").read().splitlines()

        # create a dictionary for the nodes
        node_dict = {}

        for node_set in nodes:
            # split into the current node and next nodes
            cur_node, next_nodes = node_set.split(" = ")
            node_dict[cur_node] = next_nodes[1:-1].split(', ')

        # find the positions that end with A for part 2
        a_nodes = [key for key in node_dict if key.endswith('A')]

        # store the data
        self.navi = navigation
        self.nodes = node_dict
        self.a_nodes = a_nodes

    def sim_path(self) -> int:
        """
        Simulates the route taken based on the navigation instructions
        and the nodes in the map to determine the number of nodes visited
        to go from the start to the final node ZZZ.

        Returns:
            int: the number of nodes visited
        """

        # load the data
        navi = self.navi
        nodes = self.nodes

        # initialize
        nodes_visited = 0
        current_node = 'AAA'
        scrolling_navi = navi

        # loop through nodes to find ZZZ
        while current_node != 'ZZZ':
            # increment nodes visited
            nodes_visited += 1

            # check which direction we go next
            if scrolling_navi[0] == 'L':
                node_ind = 0
            elif scrolling_navi[0] == 'R':
                node_ind = 1
            else:
                break

            # update the node
            next_node = nodes[current_node][node_ind]
            current_node = next_node

            # loop the navigation instructions
            scrolling_navi = scrolling_navi[1:] + scrolling_navi[0]

        return nodes_visited

    def parallel_sims(self) -> int:
        """
        A parallel simulation of path finding used for part 2 where
        multiple starting nodes are run at the same time and we return
        the number of steps taken

        Returns:
            int: Total number of steps taken
        """


        # load the data
        navi = self.navi
        nodes = self.nodes
        a_nodes = self.a_nodes

        # initialize
        sub_maps = []

        # loop through the different nodes
        for current_node in a_nodes:

            # initialize the required variables for the loop
            node_path = []

            scrolling_navi = navi
            nodes_visited = 0
            z_node = None

            # initialize the loop to find the paths to nodes
            while True:
                while nodes_visited == 0 or not current_node.endswith("Z"):
                    # increment nodes visited
                    nodes_visited += 1

                    # check which direction we go next
                    if scrolling_navi[0] == 'L':
                        node_ind = 0
                    elif scrolling_navi[0] == 'R':
                        node_ind = 1
                    else:
                        break

                    # update the node
                    next_node = nodes[current_node][node_ind]
                    current_node = next_node

                    # loop the navigation instructions
                    scrolling_navi = scrolling_navi[1:] + scrolling_navi[0]

                # add this to the list
                node_path.append(nodes_visited)

                # see if we hit the last node
                if z_node is None:
                    z_node = current_node
                    nodes_visited = 0
                elif current_node == z_node:
                    break

            sub_maps.append(node_path)

        counts = [sub_map[0] for sub_map in sub_maps]

        # find the lowest common multiple across the loops
        lowest_common_mult = counts.pop()

        for count in counts:
            lowest_common_mult = lowest_common_mult * count // gcd(lowest_common_mult, count)

        # return
        return lowest_common_mult

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Map('input.txt').sim_path()
    pt2_sol = Map('input.txt').parallel_sims()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
