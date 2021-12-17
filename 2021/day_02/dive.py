# https://adventofcode.com/2021/day/2

import pandas as pd


class SubInstructions():
    """
    Takes an input direction file and calculates the product of
    the forward and downwards movement

    Inputs
    ------
    file_name : string
        The name of the instruction file to be read in
    """

    def __init__(self, file_name="test.txt"):
        """
        This function reads in a text file that contains two columns.
        The first column contains the directionality and the second
        contains an integer value.
        """
        self.file_name = file_name

        # Define the column names
        self.header = ['direction', 'pos_change']

        # Read in the file using our header and specify the delimiter as space
        self.input_df = pd.read_csv(self.file_name,
                                    names=self.header,
                                    delimiter=" ")

    def forward_depth_product(self):
        """
        Solution for part 1, calculates the value given by
        forward movement * (downwards movement - upward movement)
        """
        # define a movement dataframe
        move_df = self.input_df

        # Group the rows together into their directions
        group_df = move_df.groupby("direction")['pos_change'].sum()

        total_move = group_df['forward'] * (group_df['down'] - group_df['up'])
        print(int(total_move))

    def _create_aim_col(self):
        """
        In part 2 things have complicated a bit and the submarine gets an
        additional 'aim' column that changes based on the upwards and
        downards movement.
            aim = cumulative sum of vertical movement
        """

        # define the movement dataframe
        move_df = self.input_df

        # need to define a number related to up/down direction
        map_dict = {'down': 1, 'up': -1}

        # create a new column for whether we're pointing up or down
        move_df['vert_sign'] = move_df['direction'].map(map_dict)

        # create a temp aim column that gets the aim of that row
        move_df['temp_aim'] = move_df['vert_sign'] * move_df['pos_change']

        # fill in the NaNs with 0
        move_df = move_df.fillna(0)

        # create the aim column which is the cumulative sum of temp aim
        move_df['aim'] = move_df['temp_aim'].cumsum()

        self.p2_df = move_df
    
    def aimed_product(self):
        """
        Calculate the product of the submarines movement using the additional
        aim value calculated in create_aim_col
        """

        # Generate the new dataframe with the aim column
        self._create_aim_col()

        # set the dataframe variable
        aimed_df = self.p2_df

        # calculate the depth value from aim * pos_change
        aimed_df['depth'] = aimed_df['aim'] * aimed_df['pos_change']

        # In part 2 we're only interested in rows where the sub moves forward
        forward_aimed_df = aimed_df.loc[aimed_df.direction == 'forward']

        # Now we want the sum of the horizontal position changes and
        # the depth value so we're going to drop the other columns
        fwd_depth_df = forward_aimed_df[['pos_change', 'depth']]

        # Get the sum of each column
        summed_fwd_depth_df = fwd_depth_df.sum()

        # Get the product of these two values
        tot_fwd_depth = summed_fwd_depth_df.product()

        # output
        print(int(tot_fwd_depth))