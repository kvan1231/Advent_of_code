""" https://adventofcode.com/2023/day/4 """

class Scratchcard():
    """
    Class representing the scratchcards
    """
    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Takes the input text file that contains the winning numbers
        and the users numbers in scratch cards.

        Args:
            input_file (str, optional): The text file containing the
            scratchcards and the winning numbers. Defaults to "input.txt".
        """

        # initialize lists to contain the data
        scratch_data = []
        winning_nums = []
        
        # Read in the data
        with open(input_file, 'r', encoding="utf-8") as f:
            for line in f:
                temp_nums = line.split(":")[1].strip()
                card_nums, win_nums = [
                    list(nums.split()) for nums in temp_nums.split(" | ")
                        ]
                scratch_data.append(set(card_nums))
                winning_nums.append(set(win_nums))

        # store the data
        self.scratch_data = scratch_data
        self.winning_nums = winning_nums

    def scratch_points(self) -> int:
        """
        Calculates the total points the scratch cards are worth given
        by SUM(2^(num matches - 1))

        Returns:
            int: Total points from scratch cards
        """

        # load in data
        scratch_data = self.scratch_data
        winning_nums = self.winning_nums

        # initialize output
        total_pts = 0

        # loop through the rows and find matching numbers
        for card in range(len(scratch_data)):
            num_matches = len(scratch_data[card] & winning_nums[card])

            # if we have any matches then calculate the points
            if num_matches > 0:
                card_pts = 2 ** (num_matches - 1)
            # special case of 0 pts with no matches
            else:
                card_pts = 0

            # add to total points
            total_pts += int(card_pts)

        return total_pts
    
    def total_cards(self) -> int:
        """
        Calculates the total number of scratch cards. This number is calculated
        by determining the number of winning numbers (N) in the current card and
        adding another card to the next (N) cards

        Returns:
            int: The total number of scratch cards in the lot
        """

        # load in data
        scratch_data = self.scratch_data
        winning_nums = self.winning_nums

        # initialize a list containing the number of cards
        card_count = [1] * len(scratch_data)

        # loop through the rows and find matching numbers
        for card_ind in range(len(card_count)):
            num_matches = len(scratch_data[card_ind] & winning_nums[card_ind])

            # if we have any matches then enter loop and add to the card counts
            if num_matches > 0:
                for sub_ind in range(card_ind + 1, card_ind + num_matches + 1):
                    card_count[sub_ind] = card_count[sub_ind] + card_count[card_ind]

        return sum(card_count)

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Scratchcard('input.txt').scratch_points()
    pt2_sol = Scratchcard('input.txt').total_cards()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
