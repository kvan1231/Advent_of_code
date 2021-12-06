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
        vents = self.vent_lines
        temp_grid = self.grid

        valid_x = vents.x1 == vents.x2
        valid_y = vents.y1 == vents.y2
        non_diag = valid_x | valid_y
        straight_vents = vents[non_diag]
        diag_vents = vents[~non_diag]
        if not diagonal:
            for index, rows in straight_vents.iterrows():
                # print(rows)
                # print("=========")
                x1 = rows.x1
                x2 = rows.x2
                y1 = rows.y1
                y2 = rows.y2

                if x1 == x2:
                    ymin, ymax = min(rows.y1, rows.y2), max(rows.y1, rows.y2)
                    temp_grid.loc[ymin:ymax, x1] += 1
                if y1 == y2:
                    xmin, xmax = min(rows.x1, rows.x2), max(rows.x1, rows.x2)
                    temp_grid.loc[y1, xmin:xmax] += 1
                # print(temp_grid)
                # print('\n')
        else:
            for index, rows in diag_vents.iterrows():
                # print(rows)
                # print("=========")
                x1 = rows.x1
                x2 = rows.x2
                y1 = rows.y1
                y2 = rows.y2
                xpoints = np.arange(
                    x1, x2 + np.sign(x2 - x1), np.sign(x2 - x1)
                )
                ypoints = np.arange(
                    y1, y2 + np.sign(y2 - y1), np.sign(y2 - y1)
                )
                for line_index in range(len(xpoints)):
                    xval = xpoints[line_index]
                    yval = ypoints[line_index]
                    temp_grid.loc[yval, xval] += 1
                # print(temp_grid)
                # print('\n')
        self.grid = temp_grid

    def count_overlap(self):
        """
        This function counts the number of overlaps in the
        grid drawn
        """
        overlap_cond = self.grid.ge(2)
        num_overlap = self.grid[overlap_cond].count().sum()
        return num_overlap

sol_grid = Grid("input.txt")
sol_grid.draw_vents()
sol_grid.draw_vents(diagonal=True)
sol_grid.count_overlap()