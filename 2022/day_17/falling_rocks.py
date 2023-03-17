# https://adventofcode.com/2022/day/17


class FallingRocks:
    """
    Contains the information for a falling rock sim including the shapes of
    the rocks and the movements
    """
    def __init__(self, file_name: str = 'test.txt') -> None:
        """
        This function reads in the text file that contains the rock movement
        data

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        self.rock_shapes = [
            [0, 1, 2, 3],
            [1, 1j, 1 + 1j, 2 + 1j, 1 + 2j],
            [0, 1, 2, 2 + 1j, 2 + 2j],
            [0, 1j, 2j, 3j],
            [0, 1, 1j, 1 + 1j],
        ]

        with open(file_name) as f:
            raw_data = f.read().strip()

        self.movement_pattern = [1 if x == ">" else -1 for x in raw_data]

        # The ground is represented as a set of tuples with a y coordinate of
        # -1
        self.ground = {x - 1j for x in range(7)}

        # The current height of the rock is initialized to zero
        self.rock_height = 0

        # A counter for the number of rocks that have landed on the ground
        self.rock_count = 0

        # The index of the current rock shape in the rock_shapes list
        self.rock_shapes_index = 0

        # Store the rock positions as a set of tuples
        self.rock = {
            x + 2 + (self.rock_height + 3) * 1j for x in
            self.rock_shapes[self.rock_shapes_index]
        }

    def part1_sim(self, num_steps: int = 2022) -> int:
        """
        Simulates the rocks falling in part 1 of the advent of code problem
        based on the number of steps required
        """

        # initialize
        rock_shapes = self.rock_shapes
        movement_pattern = self.movement_pattern

        ground = self.ground
        height = self.rock_height
        rock_count = self.rock_count

        rock_index = self.rock_shapes_index
        rock = self.rock

        # loop through the sim
        while rock_count < num_steps:

            # loop through the moves
            for move in movement_pattern:

                # Move the rock according to the movement_pattern
                moved = {x + move for x in rock}

                # If the moved rock is within the bounds of the game and does
                # not collide with the ground, update the rock_positions
                if all(0 <= x.real < 7 for x in moved) and not \
                        (moved & ground):
                    rock = moved

                # new position
                moved = {x - 1j for x in rock}

                # check if collide with ground
                if moved & ground:
                    ground |= rock
                    rock_count += 1
                    height = max(x.imag for x in ground) + 1

                    # break once we've simulated enough
                    if rock_count >= num_steps:
                        break

                    # update to next rock
                    rock_index = (rock_index + 1) % 5

                    rock = {
                        x + 2 + (height + 3) * 1j for x in
                        rock_shapes[rock_index]
                    }

                # If the rock does not collide with the ground, update the
                # rock_positions
                else:
                    rock = moved

        # return the height
        return int(height)

    def part2_sim(self, num_steps: int = 1000000000000) -> int:
        """
        Simulates the rocks falling in part 2 of the advent of code problem
        based on the number of steps required. Due to the sheer number of steps
        we cant brute force it. Following Hyperneutrino's tutorial he noticed
        that there is a pattern in the output so by finding that pattern and
        storing it somewhere we can cut down on the required compute power
        """

        # initialize
        rock_shapes = self.rock_shapes
        movement_pattern = self.movement_pattern

        ground = self.ground
        height = self.rock_height
        rock_count = self.rock_count

        rock_index = self.rock_shapes_index
        rock = self.rock

        offset = 0
        seen_states = {}

        # loop through the sim
        while rock_count < num_steps:

            # loop through the moves
            for move_ind, move in enumerate(movement_pattern):

                # Move the rock according to the movement_pattern
                moved = {x + move for x in rock}

                # If the moved rock is within the bounds of the game and does
                # not collide with the ground, update the rock_positions
                if all(0 <= x.real < 7 for x in moved) and not \
                        (moved & ground):
                    rock = moved

                # new position
                moved = {x - 1j for x in rock}

                # check if collide with ground
                if moved & ground:
                    ground |= rock
                    rock_count += 1
                    height = max(x.imag for x in ground) + 1

                    # break once we've simulated enough
                    if rock_count >= num_steps:
                        break

                    # update to next rock
                    rock_index = (rock_index + 1) % 5

                    rock = {
                        x + 2 + (height + 3) * 1j for x in
                        rock_shapes[rock_index]
                    }

                    # create this new key
                    key = (move_ind, rock_index, self._summarize())

                    # if we've seen this config
                    if key in seen_states:

                        # get the previous values
                        last_rock_count, last_height = seen_states[key]

                        # find the remaining steps
                        remain = num_steps - rock_count

                        # find the repititions by determining the cycle size
                        reps = remain // (rock_count - last_rock_count)

                        # calculate the offset using height gained in a cycle
                        offset = reps * (height - last_height)

                        # make a jump in rock count based on the cycle size
                        rock_count += reps * (rock_count - last_rock_count)
                        seen_states = {}
                    # add it to seen states
                    seen_states[key] = (rock_count, height)

                # If the rock does not collide with the ground, update the
                # rock_positions
                else:
                    rock = moved

        # return the height
        return int(height + offset)

    def _summarize(self):

        ground = self.ground
        # check the last 20 values
        old = [-20] * 7

        for x in ground:
            real = int(x.real)
            imag = int(x.imag)
            old[real] = max(old[real], imag)

        top = max(old)
        return tuple(x - top for x in old)


def solution():
    pt1_sol = FallingRocks('input.txt').part1_sim()
    pt2_sol = FallingRocks('input.txt').part2_sim()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)