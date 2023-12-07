""" https://adventofcode.com/2023/day/5 """

class Almanac():
    """
    Class representing the almanac for seeds to be planted
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Takes the input text file that contains the seeds of plans to be planted
        along with the seed-to-soil, soil-to-fertilizer, fertilizer-to-water,
        water-to-light, light-to-temperature, temperature-to-humidity and
        humidity-to-location

        Args:
            input_file (str, optional): Text file containing all of the relevant
            seed and plant properties. Defaults to "input.txt".
        """

        # Read in the data
        seeds, *maps = open(input_file, encoding="utf-8").read().split('\n\n')

        # split the seeds into a list
        seed_list = list(
            map(int, seeds.split(":")[1].strip().split())
            )

        self.seed_list = seed_list
        self.maps = maps

    def find_low_location(self) -> int:
        """
        Follows the mapping from a given starter seed to determine the seed
        with the lowest location number

        Returns:
            int: lowest location number
        """

        # load data
        seed_list = self.seed_list
        maps = self.maps

        # loop through the maps
        for item_map in maps:
            item_ranges = []

            # find the map ranges in each item
            for map_values in item_map.splitlines()[1:]:
                item_ranges.append(
                    list(map(int, map_values.split()))
                )

            # create a list to track a map from seed to location
            temp_map = []

            # loop through the seeds
            for seed in seed_list:
                # get the destination range start, source range start and range length
                for drs, srs, rl in item_ranges:
                    if srs <= seed < srs + rl:
                        temp_map.append(seed - srs + drs)
                        break

                else:
                    temp_map.append(seed)
            seed_list = temp_map

        return min(seed_list)

    def find_low_loc_range(self) -> int:
        """
        Follows the mapping from a given starter seed range to 
        determine the initial seed with the lowest location number

        Returns:
            int: lowest location number
        """

        # load data
        seed_range = self.seed_list
        maps = self.maps

        # initialize seed list
        seed_list = []

        for seed_ind in range(0, len(seed_range), 2):
            seed_list.append(
                (seed_range[seed_ind],
                 seed_range[seed_ind] + seed_range[seed_ind + 1])
            )

        # loop through the maps
        for item_map in maps:
            item_ranges = []

            # find the map ranges in each item
            for map_values in item_map.splitlines()[1:]:
                item_ranges.append(
                    list(map(int, map_values.split()))
                )

            # create a list to track a map from seed to location
            temp_map = []

            # need an additional loop for our new list of seeds
            while len(seed_list) > 0:

                # find the seed range start and end points
                start_seed, end_seed = seed_list.pop()

                # again get the destination range start,
                # source range start and range length
                for drs, srs, rl in item_ranges:

                    # determine a starting and end point for range
                    start_val = max(start_seed, srs)
                    end_val = min(end_seed, srs + rl)

                    # for a valid combination
                    if start_val < end_val:

                        # append the maps from seed to end
                        temp_map.append((start_val - srs + drs, end_val - srs + drs))
                        if start_val > start_seed:
                            seed_list.append((start_seed, start_val))
                        if end_seed > end_val:
                            seed_list.append((end_val, end_seed))
                        break
                else:
                    temp_map.append((start_seed, end_seed))
            seed_list = temp_map

        # return
        return min(seed_list)[0]

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Almanac('input.txt').find_low_location()
    pt2_sol = Almanac('input.txt').find_low_loc_range()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
