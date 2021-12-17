# https://adventofcode.com/2021/day/12


# We're going to be use collections.defaultdict
# so we can add to the dictionary whenever its
# missing a key instead of throwing an error
from collections import defaultdict

# initialize the defaultdict
connected_cave = defaultdict(list)

# read in the data
file_name = "input.txt"
for line in open(file_name, 'r').readlines():

    # split the lines at the -
    start, end = line.strip().split("-")

    # the first element is the start and connect
    # it to the "end"
    connected_cave[start] += [end]

    # add the opposite direction
    connected_cave[end] += [start]


# find all of the paths
def path_search(seen_caves=set(),
                cur_cave='start',
                part=1):
    """
    define the seen locations as a set
    define the starting position as 'start' for the path
    define the part of the function depending if 
    we're solving for p1 or p2
    """

    # if our position is an 'end' position, stop
    if cur_cave == 'end':
        return 1

    # if we've entered the cave before
    if (cur_cave in seen_caves):
        # if the cave is the start, end
        if cur_cave == 'start':
            return 0
        # if the cave is a small cave
        if cur_cave.islower():
            # if its part 1, end
            if part == 1:
                return 0
            # if its not part 1, change next
            # iteration to part 1 so we only
            # visit the cave twice max
            else:
                part = 1

    # add the current cave to the seen set
    seen_caves = seen_caves | {cur_cave}

    # initialize a list to keep the paths
    list_paths = 0

    # loop through all our connected caves
    for neighbour in connected_cave[cur_cave]:
        # add another path to the list of paths
        list_paths += path_search(
            seen_caves, neighbour, part
        )

    return list_paths


part_1_paths = path_search()
part_2_paths = path_search(part=2)
print("part 1 solution:", part_1_paths)
print("part 2 solution:", part_2_paths)