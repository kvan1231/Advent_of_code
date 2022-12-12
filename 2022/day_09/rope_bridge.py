# https://adventofcode.com/2022/day/9


class Rope():
    """
    This class will contain the instructions that the rope will move in
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the heights

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split('\n')

        self.instructions = raw_data

    def tail_visits(self) -> tuple:
        """
        Counts the positions the tail visits at least once when it is one
        knot long and ten knots long
        """

        instructions = self.instructions

        # move the rope around
        ten_knot = one_knot = list(
            self.tail_move(self.head_move(instructions))
            )

        # check for only unique positions when the tail is one knot long
        one_knot_count = len(set(one_knot))

        # calculate the positions with ten knots
        for _ in range(8):
            ten_knot = self.tail_move(ten_knot)

        ten_knot_count = len(set(ten_knot))

        return one_knot_count, ten_knot_count

    def head_move(self, instructions: list):
        """
        Reads in a list of instructions and moves the head appropriately
        """

        # intialize
        hori = 0
        vert = 0

        # loop through the instructions
        for command in instructions:

            # split into direction and magnitude
            direction, magnitude = command.split()

            # update the vertial and horizontal values
            for _ in range(int(magnitude)):
                hori += (direction == 'R') - (direction == 'L')
                vert += (direction == 'U') - (direction == 'D')
                yield hori, vert

    def tail_move(self, head_position):
        """
        Reads in a list of head positions and moves the tail appropriately
        """

        # intialize
        hori = 0
        vert = 0

        # loop through the head_positions
        for head_values in head_position:

            # split into direction and magnitude
            head_hori, head_vert = head_values

            # check if the head position is more than 1 space away
            if abs(head_hori - hori) > 1 or abs(head_vert - vert) > 1:
                """
                doing math with booleans to decide if we go left or right
                explanation:
                if the head position is further right then
                    head_hori > hori = true (1)
                    head_hori < hori = false (0)
                which tells our tail position that it needs to move right
                if the head is further left then
                    head_hori > hori = false (0)
                    head_hori < hori = true (1)
                which gives us a negative number when we do the following math
                """
                hori += (head_hori > hori) - (head_hori < hori)

                # do the same math for vertical position
                vert += (head_vert > vert) - (head_vert < vert)

            yield hori, vert


def solution():
    pt1_sol, pt2_sol = Rope('input.txt').tail_visits()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
