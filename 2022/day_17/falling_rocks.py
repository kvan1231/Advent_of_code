# https://adventofcode.com/2022/day/16


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
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ]

        with open(file_name) as f:
            raw_data = f.read().strip()

        self.movement_pattern = [1 if x == ">" else -1 for x in raw_data]

        # The ground is represented as a set of tuples with a y coordinate of
        # -1
        self.ground = {(x, -1) for x in range(7)}

        # The current height of the rock is initialized to zero
        self.rock_height = 0

        # A counter for the number of rocks that have landed on the ground
        self.rock_count = 0

        # The index of the current rock shape in the rock_shapes list
        self.rock_shape_index = 0

        # Store the rock positions as a set of tuples
        self.rock_positions = set(self.rock_shapes[self.rock_shape_index])

    def step(self):
        # Move the rock according to the movement_pattern
        moved_rock_positions = {
            (
                x + self.movement_pattern[
                    self.rock_count % len(self.movement_pattern)
                ], y
                ) for x, y in self.rock_positions
        }

        # If the moved rock is within the bounds of the game and does not
        # collide with the ground, update the rock_positions
        if all(0 <= x < 7 for x, _ in moved_rock_positions) and not \
            (moved_rock_positions & self.ground):
            self.rock_positions = moved_rock_positions

        # Otherwise, move the rock down one unit
        else:
            moved_rock_positions = {(x, y - 1) for x, y in self.rock_positions}
            # If the rock collides with the ground, add it to the ground and
            # update the rock_height

            if moved_rock_positions & self.ground:
                self.ground |= self.rock_positions
                self.rock_count += 1
                self.rock_height = max(y for _, y in self.ground) + 1

                # Select the next rock shape and reset the rock_positions
                self.rock_shape_index = (self.rock_shape_index + 1) % 5

                self.rock_positions = set(
                    self.rock_shapes[self.rock_shape_index]
                    )
            # If the rock does not collide with the ground, update the
            # rock_positions
            else:
                self.rock_positions = moved_rock_positions

# Create a RockGame object with the given rock shapes and movement pattern
pt1_sim = FallingRocks()


# Step the game 2022 times
for _ in range(2022):
    pt1_sim.step()
    print(pt1_sim.rock_height)
