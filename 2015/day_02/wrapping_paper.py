# https://adventofcode.com/2015/day/2

import pandas as pd


class wrapping_paper():
    def __init__(self, input_file='input.txt'):
        """
        Read in the data and generate the areas of each side
        of the boxes
        """

        box_dim_list = pd.read_csv(
            input_file, delimiter='x', header=None,
            names=['l', 'w', 'h'], dtype=int
        )

        # calculate the areas of the sides
        box_dim_list['lw'] = box_dim_list['l'] * box_dim_list['w']
        box_dim_list['wh'] = box_dim_list['w'] * box_dim_list['h']
        box_dim_list['hl'] = box_dim_list['h'] * box_dim_list['l']

        self.box_dim_list = box_dim_list

    def calc_wrapping_paper(self):
        """
        Calculate the total area of wrapping paper needed
        """
        box_dim_list = self.box_dim_list

        # keep only the areas of each side
        sub_dim_list = box_dim_list[['lw', 'wh', 'hl']]

        # get the total area necessary for the box
        area_per_box = sub_dim_list.sum(axis=1) * 2

        # get the padding value which is the smallest area
        padding = sub_dim_list.min(axis=1)

        # add the padding to the area per box and sum over entire series
        tot_area = (area_per_box + padding).sum()

        return tot_area

    def calc_ribbon_length(self):
        """
        Calculate the total length of ribbon needed where the length of the
        ribbon wrapped around the box is:
            2 * SUM(2 shortest sides)
        OR:
            2 * [SUM(all sides) - longest side]
        the length of the ribbon needed for the bow is:
            PRODUCT(all sides)
        """

        box_dim_list = self.box_dim_list

        # keep the length, width and height of each box
        sub_dim_list = box_dim_list[['l', 'w', 'h']]

        # calculate the length of the ribbon needed to wrap around each box
        max_dim = sub_dim_list.max(axis=1)
        wrapping_length = 2 * (sub_dim_list.sum(axis=1) - max_dim)

        # calculate the length of ribbon for the bow for each box
        bow_length = sub_dim_list.product(axis=1)

        # calculate the total amount of ribbon needed
        total_length = (wrapping_length + bow_length).sum()

        return total_length
