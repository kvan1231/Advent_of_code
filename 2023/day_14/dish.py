""" https://adventofcode.com/2023/day/14 """

class Platform():
    """
    A class containing the data for the rocks on the platform
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file and extracts the raw data

        Parameters
        ----------
        input_file : str, optional
            The text file containing the grid information for the rocks
            the 'O' denote movable rocks, '#' stationary rocks and '.' are
            points on the grid where there are no rocks, by default "input.txt"
        """

        # read in the data as a tuple
        grid = tuple(open(input_file, 'r', encoding='utf-8').read().splitlines())

        # keep the data
        self.init_grid = grid

        # a few more useful variables for the spin cycle later
        self.grid = grid
        self.grid_set = {grid}
        self.grid_list = [grid]

    def tilt_grid(self) -> tuple:
        """
        Tilts the grid and repositions the rocks

        Returns
        -------
        tuple
            The new grid that consists of a tuple of strings after tilting
            the grid towards the north and having the rocks reposition
        """
        # get the initial grid
        init_grid = self.grid

        # swap the columns and rows so its easier to roll
        flip_grid = tuple(map("".join, zip(*init_grid)))

        # intialize the grid where we roll the rocks
        roll_grid = []

        # roll the rocks
        for row in flip_grid:
            # split the row into chunks at the immovable rocks '#'
            rock_chunks = row.split("#")

            # initalize a list to contain the chunks after rollowing
            rolled_chunks = []

            # go through the split sections of the row
            for chunk in rock_chunks:
                rolled_chunk = "".join(sorted(chunk, reverse=True))
                rolled_chunks.append(rolled_chunk)

            # add the stationary rocks back in
            rolled_row = "#".join(rolled_chunks)

            # add the row to the grid
            roll_grid.append(rolled_row)

        # convert to tuple
        roll_grid = tuple(roll_grid)

        return roll_grid

    def _cycle(self) -> None:
        """
        Runs the grid through a spin cycle where we tilt the grid North, West
        South then East to complete one cycle. After each tilt the rocks are
        allowed to roll to their resting positon

        Returns
        -------
        None
            Just runs the cycle
        """

        for _ in range(4):
            grid = self.tilt_grid()
            grid = tuple(row[::-1] for row in grid)
            self.grid = grid

    def sim_cycles(self) -> int:
        """
        Simulates the spin cycles of the platform until we've exhausted all
        combinations. We expect that at some point when we tilt the platform
        we will recreate a grid that has already been seen

        Returns
        -------
        int
            The number of iterations it took to find all formations
        """

        # initilize
        iteration = 0

        grid_set = self.grid_set
        grid_list = self.grid_list

        # start the loop
        while True:
            iteration += 1
            self._cycle()

            # look at the new grid
            new_grid = self.grid
            # if we've seen this grid before then break
            if new_grid in self.grid_set:
                return iteration

            grid_set.add(new_grid)
            grid_list.append(new_grid)

            self.grid_set = grid_set
            self.grid_list = grid_list

    def calc_tilt_load(self) -> int:
        """
        Calculates the total load on the north support beams after
        the grid of rocks rolled

        Returns
        -------
        int
            The total load on the beam
        """

        # grab the tilted grid
        roll_grid = self.tilt_grid()

        # flip the columns and rows again
        tilted_grid = tuple(map("".join, zip(*roll_grid)))

        # initialize
        total_load = 0

        # get the total number of rows
        total_rows = len(tilted_grid)

        # calculate the load per row
        for index, row in enumerate(tilted_grid):
            rock_count = row.count("O")
            rock_weight = total_rows - index
            row_load = rock_count * rock_weight

            total_load += row_load

        return total_load

    def calc_cycle_load(self, num_sims:int = int(1e9)) -> int:
        """
        Runs the platform through the cycle and calculates
        the load on the north support beam 
        
        Parameters
        ----------
        num_sims : int, optional
            the number of times we want to run the cycle, by default int(1e9)

        Returns
        -------
        int
            The total load on the beam
        """

        # cycle the grid
        iterations = self.sim_cycles()

        grid_list = self.grid_list
        grid = self.grid

        # initialize
        total_load = 0

        # get the occurance of our starter grid to determine our starting point in the list of grid
        first_ind = grid_list.index(grid)

        # get the grid from our grid list based on the number of simulations
        output_grid = grid_list[
            (num_sims - first_ind) % (iterations - first_ind) + first_ind
        ]

        # get the total number of rows
        total_rows = len(output_grid)

        # calculate the load per row
        for index, row in enumerate(output_grid):
            rock_count = row.count("O")
            rock_weight = total_rows - index
            row_load = rock_count * rock_weight

            total_load += row_load

        return total_load

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Platform().calc_tilt_load()
    pt2_sol = Platform().calc_cycle_load()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
