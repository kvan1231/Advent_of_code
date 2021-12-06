# https://adventofcode.com/2021/day/5

import pandas as pd
import numpy as np


class Grid():
    """
    This class will contain the grid and update according
    to the inputs to show where the hydrothermal vents are

    Inputs
    ------
    input_name : string
        The hydrothermal vent end points
    """

    def __init__(self, input_name="test.txt"):
        """
        Reads in the data and properly cleans it to be
        used in later functions
        """
        # Read in the data and split once
        input_data = pd.read_csv(
            input_name, header=None, sep=" -> ",
            engine='python'
        )

        # split the data again into init and final coordinate
        coords1 = input_data[0].str.split(",", expand=True)
        coords2 = input_data[1].str.split(",", expand=True)

        # Recombine the data
        data_inputs = pd.concat([coords1, coords2], axis=1)

        # Set the column names
        data_inputs.columns = ['x1', 'y1', 'x2', 'y2']

        # Store the grid lines
        self.vent_lines = data_inputs.astype(int)

        # Get the largest number to make our grid
        max_grid_len = self.vent_lines.max().max()

        # Generate the grid
        self.grid = pd.DataFrame(
            0, index=range(max_grid_len + 1),
            columns=range(max_grid_len + 1)
        )

    def draw_vents(self, diagonal=False):
        """
        This function takes the inputted data and
        draws the hydrothermal vents on our initialized
        grid
        """
        # pull the required properties
        vents = self.vent_lines
        temp_grid = self.grid

        # check where the horizontal and vertical lines are
        valid_x = vents.x1 == vents.x2
        valid_y = vents.y1 == vents.y2

        # create the index for "non diagonal" lines
        non_diag = valid_x | valid_y

        # non diagonal rows
        straight_vents = vents[non_diag]

        # diagonal rows
        diag_vents = vents[~non_diag]

        # loop through the horizontal and vertical lines
        if not diagonal:

            # loop through the rows
            for index, rows in straight_vents.iterrows():
                # print(rows)
                # print("=========")
                x1 = rows.x1
                x2 = rows.x2
                y1 = rows.y1
                y2 = rows.y2

                # determine if the line is vert or hori
                if x1 == x2:
                    # find the start and end points
                    ymin, ymax = min(rows.y1, rows.y2), max(rows.y1, rows.y2)

                    # increment the cells
                    temp_grid.loc[ymin:ymax, x1] += 1
                if y1 == y2:

                    # find the start and end points
                    xmin, xmax = min(rows.x1, rows.x2), max(rows.x1, rows.x2)

                    # increment
                    temp_grid.loc[y1, xmin:xmax] += 1
                # print(temp_grid)
                # print('\n')
        # diagonal lines
        else:
            for index, rows in diag_vents.iterrows():
                # print(rows)
                # print("=========")
                x1 = rows.x1
                x2 = rows.x2
                y1 = rows.y1
                y2 = rows.y2

                # use numpy arange to get the order of the numbers
                xpoints = np.arange(
                    x1, x2 + np.sign(x2 - x1), np.sign(x2 - x1)
                )
                ypoints = np.arange(
                    y1, y2 + np.sign(y2 - y1), np.sign(y2 - y1)
                )

                # need to loop through the numbers or pandas
                # will take these values and drawn a square
                # bounded by the indices
                for line_index in range(len(xpoints)):

                    # go to that cell and increment
                    xval = xpoints[line_index]
                    yval = ypoints[line_index]
                    temp_grid.loc[yval, xval] += 1
                # print(temp_grid)
                # print('\n')
        # replace the internal grid
        self.grid = temp_grid

    def count_overlap(self):
        """
        This function counts the number of overlaps in the
        grid drawn
        """
        # if any grid cell is greater than or equal to two then
        # there was overlap
        overlap_cond = self.grid.ge(2)

        # count the number of cells where the number is greater than
        # or equal to 2
        num_overlap = self.grid[overlap_cond].count().sum()
        return num_overlap

# run the solution for part 2
sol_grid = Grid("input.txt")
sol_grid.draw_vents()

# comment this line out for part 1 solution
sol_grid.draw_vents(diagonal=True)

# return solution
sol_grid.count_overlap()