# https://adventofcode.com/2021/day/4

"""
The input file for this challenge consists two sets of data that
need to be read in differently
1. a long row of numbers in the order that they're drawn in for bingo
2. individual bingo boards of each player in a 5x5 grid
I couldn't come up with an efficient way of reading in these two
disparate data formats so this code only works if you manually split
these files first

test.txt is split into

test_draws.txt - this file contains the numbers drawn
test_boards.txt - this file contains the bingo boards

"""

import pandas as pd


class BingoBoard():
    """
    This class will contain all of the information related to
    a bingo board.

    Inputs
    ------
    file_name : string
        The name of the input file to be read in
    """

    # Keep track of last number drawn
    last_number = None

    def __init__(self, input_board):
        """
        This function takes in a 5x5 pandas dataframe
        that contains the numbers in a bingo board.
        """

        # Generate a dataframe with all of the boards
        self.num_board = input_board.astype(int)

        # reset the row index
        self.num_board.index = range(5)

        # print(self.num_board)
        # Create a success board that tracks if a number
        # was drawn
        self.drawn_board = pd.DataFrame(
            0, index=range(len(self.num_board)),
            columns=range(len(self.num_board))
        )

    def check_win(self):
        """
        This function checks if the sum of a row or
        column equals to 5. Normal bingo accounts
        for diagonals as well but this game only checks
        for rows and columns. If the row or column
        equals to 5 in our 'drawn_board' then we
        have a bingo.
        """
        column_check = 5 in self.drawn_board.sum(axis=0).values
        row_check = 5 in self.drawn_board.sum(axis=1).values

        if (row_check or column_check):
            filter_cond = self.drawn_board == 0
            undrawn_nums = self.num_board.where(filter_cond)
            tot_undrawn = int(undrawn_nums.sum().sum())
            # self.total_undrawn = tot_undrawn
            return tot_undrawn

    def num_drawn(self, number):
        """
        This function updates the drawn_board dataframe
        where a number is drawn in the num_board dataframe
        """
        if not self.check_win():
            self.last_num = number
            filter_cond = self.num_board == number
            self.drawn_board[filter_cond] = 1


# read in the boards
board_file = "input_boards.txt"
all_boards = pd.read_csv(
    board_file, header=None, delim_whitespace=True
)

# read in the draws
draw_file = "input_draws.txt"
with open(draw_file) as f:
    draws = f.readlines()

# MAKE SURE THE DRAWS OR INTS OR PYTHON MIGHT NOT EQUATE THE DRAWS TO BOARDS
draw_list = [int(num.strip()) for num in draws[0].split(',')]

# determine how many boards there are
board_list = []
num_boards = int(len(all_boards) / 5)

# Loop through the boards and split it into a list
board_index = 0
for temp_index in range(num_boards):
    start_ind = board_index
    end_ind = board_index + 5

    temp_board = BingoBoard(all_boards[start_ind:end_ind])
    board_list.append(
        temp_board
    )

    board_index += 5

# Create an empty array of winning boards to parse later
winning_boards = []
temp_list = board_list

# start looping through the draws
for draw in draw_list:
    # print(draw)
    # loop through each board
    for board_index in range(len(board_list)):
        board = board_list[board_index]
        # draw the number and apply to board
        board.num_drawn(int(draw))
        # print(summed_value)

        # If a board wins then print the last drawn number, the
        # sum of the remaining positions and the product of these
        # two values
        summed_value = board.check_win()
        if summed_value:
            # print(board.last_num)
            # print("=============")
            # print(board.num_board)
            # print(board.drawn_board)

            # print(f"sum {summed_value}, draw {draw}, {summed_value * draw}")
            # board_list.remove(board)
            # winning_boards.append(board)
            """
            the original plan was to append winning boards to a new
            list and remove boards that had won. This could only solve
            part 1 of the problem and would always result in odd indexing
            issues for part 2. If anyone knows why this method fails please
            let me know.
            """
            winning_boards.append([board_index, summed_value, draw])

# Convert the list of winning boards to Dataframe
winning_df = pd.DataFrame(
    winning_boards, columns=['board_index', 'summed_value', 'draw']
)

# Filter the board indexes that we've defined to only the unique values
# Pandas does this in order
winning_order = winning_df['board_index'].unique()

# the first board that wins appears first in this list and the last board last
first_win = winning_order[0]
last_win = winning_order[-1]

# Get the rows that contain information about the first and last boards
first_win_rows = winning_df['board_index'] == first_win
last_win_rows = winning_df['board_index'] == last_win

# Grab the first appearance of these boards
first_board = winning_df.loc[first_win_rows].iloc[0][['summed_value', 'draw']]
last_board = winning_df.loc[last_win_rows].iloc[0][['summed_value', 'draw']]

# Calculate the product of these rows
first_product = first_board.product()
last_product = last_board.product()