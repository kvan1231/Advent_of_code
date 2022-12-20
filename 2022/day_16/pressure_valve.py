# https://adventofcode.com/2022/day/16

from collections import deque


class Valve():
    """
    Contains the information related to each valve such as the flow rate and
    where it flows to
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the valve data and
        processes the data to be used

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # initialize
        self.valves = {}
        self.tunnels = {}

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().splitlines()

        for valve_line in raw_data:

            # grab the valve name
            valve = valve_line.split()[1]

            # get the flow rate
            flow_rate = int(valve_line.split('=')[1].split(';')[0])

            # get where the valves tunnel to
            target = valve_line.split('to ')[1].split(" ", 1)[1].split(', ')

            self.valves[valve] = flow_rate
            self.tunnels[valve] = target

        # Initialize a dictionary to store distance information
        self.dists = {}

        # Initialize a list to store non-empty valves
        self.nonempty = []

        # Calculate the distance between each valve to all other valves and AA
        for valve in self.valves:
            # Skip empty valves that are not AA
            if valve != "AA" and not self.valves[valve]:
                continue

            # Add the non-empty valve to the list
            if valve != "AA":
                self.nonempty.append(valve)

            # Initialize a dictionary to store the distance from the current
            # valve to all other valves
            self.dists[valve] = {valve: 0, "AA": 0}

            # Initialize a set to store visited valves
            visited = {valve}

            # Initialize the queue with the current valve as the starting
            # position
            queue = deque([(0, valve)])

            # Continue until the queue is empty
            while queue:

                # Remove the first element from the queue
                distance, position = queue.popleft()

                # Explore all neighbors of the current position
                for neighbor in self.tunnels[position]:

                    # Skip already visited neighbors
                    if neighbor in visited:
                        continue

                    # Mark the neighbor as visited
                    visited.add(neighbor)

                    # Calculate the distance to the neighbor and store it in
                    # the dists dictionary
                    if self.valves[neighbor]:
                        self.dists[valve][neighbor] = distance + 1

                    # Add the neighbor to the queue to be explored in the next
                    # iteration
                    queue.append((distance + 1, neighbor))

            # Remove the distance from the valve to itself
            del self.dists[valve][valve]

            # Remove the distance from the valve to AA if the valve is not AA
            if valve != "AA":
                del self.dists[valve]["AA"]

        # Initialize a dictionary to store the indices of the non-empty valves
        # in the list
        self.indices = {}

        # Populate the indices dictionary
        for index, element in enumerate(self.nonempty):
            self.indices[element] = index

        # Initialize a cache to store previously calculated results
        self.cache = {}

    def pressure_release(self,
                         time: int = 30,
                         valve: str = "AA",
                         bitmask: int = 0) -> int:
        """
        Calculates the amount of pressure that could be released in the time
        inputted

        Parameters
        ----------
        time: int
            The amount of time to run the simulation for before calculating
            the total pressure released

        valve: str
            The starting valve

        bitmask: int
            Tracks the valves that have already been visited in bit form
        """

        # Initialize
        cache = self.cache
        dists = self.dists
        indices = self.indices
        valves = self.valves

        # Return the result from the cache if it exists
        if (time, valve, bitmask) in cache:
            return cache[(time, valve, bitmask)]

        # Initialize a variable to store the maximum flow
        max_pressure = 0

        # Calculate the maximum flow through each neighbor of the current valve
        for neighbor in dists[valve]:

            # Get the index of the neighbor in the non-empty valves list
            bit = 1 << indices[neighbor]

            # Skip neighbors that have already been visited
            if bitmask & bit:
                continue

            # Calculate the remaining time after visiting the neighbor
            remaining_time = time - dists[valve][neighbor] - 1

            # Skip neighbors that cannot be reached in the remaining time
            if remaining_time <= 0:
                continue

            # Calculate the maximum flow through the neighbor and add
            max_pressure = max(max_pressure,
                               self.pressure_release(remaining_time,
                                                     neighbor,
                                                     bitmask | bit)
                               + valves[neighbor] * remaining_time)

        cache[(time, valve, bitmask)] = max_pressure
        return max_pressure

    def part1(self) -> int:
        """
        Calculates the max pressure release at 30 minutes
        """

        max_pressure = self.pressure_release(30, "AA", 0)
        return max_pressure

    def part2(self):
        """
        Calculates the max pressure release with an elephant helping
        """

        # Calculate the maximum possible bitmask value
        max_bitmask = (1 << len(self.nonempty)) - 1

        max_pressure = 0

        # iterate over the possible bitmask values
        for bitval in range((max_bitmask + 1) // 2):

            # we're going to use the caret to get the other half of the
            # possibilities
            pressure = self.pressure_release(
                26, "AA", bitval
            ) + self.pressure_release(
                26, "AA", max_bitmask ^ bitval
            )

            max_pressure = max(max_pressure, pressure)

        return max_pressure


def solution():
    pt1_sol = Valve('input.txt').part1()
    pt2_sol = Valve('input.txt').part2()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

