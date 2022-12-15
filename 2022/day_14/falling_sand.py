# https://adventofcode.com/2022/day/14


class Sand():
    """
    Contains the coordinates of the various ends of the walls and functions
    that simulate sand flowing downwards into the walls
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the wall coordinates

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # define an empty set to contain the walls
        walls = set()

        # create an value for the abyss where the sand falls away
        abyss = 0

        # read in the dataS
        with open(file_name) as f:
            raw_data = f.read().splitlines()

        # convert the raw data into x and y positions for the walls
        for wall_data in raw_data:

            # split the pairs to find the starting and end points
            wall_ends = wall_data.split(' -> ')

            # group them together
            for pair1, pair2 in list(zip(wall_ends, wall_ends[1:])):

                # convert the values into ints
                x1, y1 = list(map(int, pair1.split(',')))
                x2, y2 = list(map(int, pair2.split(',')))

                # sort the values
                startx, endx = sorted([x1, x2])
                starty, endy = sorted([y1, y2])

                # loop to add them to our wall set
                for x in range(startx, endx + 1):
                    for y in range(starty, endy + 1):
                        walls.add((x, y))
                        abyss = max(abyss, y + 1)

        self.walls = walls
        self.abyss = abyss

    def simulate_part1(self) -> int:
        """
        Simulates falling sand from 500, 0 until sand falls into the abyss
        outputs the amount of sand particles that get added to the sim
        """

        walls = self.walls
        abyss = self.abyss

        # total number of sand particles
        total_sand = 0

        # continue to simulate
        while True:

            # initial sand starting position
            sandx, sandy = 500, 0

            while True:

                if sandy >= abyss:
                    return total_sand

                # can the sand fall straight down
                if (sandx, sandy + 1) not in walls:
                    sandy += 1
                    continue

                # can the sand fall diagonally to the left
                if (sandx - 1, sandy + 1) not in walls:
                    sandx -= 1
                    sandy += 1
                    continue

                # can the sand fall diagonally to the right
                if (sandx + 1, sandy + 1) not in walls:
                    sandx += 1
                    sandy += 1
                    continue

                # add the sand particle to the set of walls
                walls.add((sandx, sandy))
                total_sand += 1
                break

    def simulate_part2(self) -> int:
        """
        Simulates falling sand from 500, 0 until sand comes to rest at 500, 0
        and outputs the total amount of sand created
        """

        walls = self.walls
        abyss = self.abyss

        # total number of sand particles
        total_sand = 0

        # continue to simulate
        while (500, 0) not in walls:

            # initial sand starting position
            sandx, sandy = 500, 0

            while True:

                if sandy >= abyss:
                    break

                # can the sand fall straight down
                if (sandx, sandy + 1) not in walls:
                    sandy += 1
                    continue

                # can the sand fall diagonally to the left
                if (sandx - 1, sandy + 1) not in walls:
                    sandx -= 1
                    sandy += 1
                    continue

                # can the sand fall diagonally to the right
                if (sandx + 1, sandy + 1) not in walls:
                    sandx += 1
                    sandy += 1
                    continue
                break

            # add the sand particle to the set of walls
            walls.add((sandx, sandy))
            total_sand += 1

        return total_sand


def solution():
    pt1_sol = Sand('input.txt').simulate_part1()
    pt2_sol = Sand('input.txt').simulate_part2()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
