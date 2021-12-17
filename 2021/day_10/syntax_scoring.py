# https://adventofcode.com/2021/day/10

# let's create a dictionary of the pairs of brackets
pairs = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

# Creating a dictionary of the points associated with each bracket
# in part 1
part1_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

# Creating a dictionary of the points associated with each bracket
# in part 2
part2_points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

# Initialize the variable to store the total points for part 1
total_points_p1 = 0

# Initalize the list to store the points for part 2
list_points_p2 = []

input_file = 'input.txt'
# loop through the file and grab each line
for line in open(input_file):
    # initialize a list to store pairs
    temp_list = []

    # create a flag to determine if the line is corrupted (True)
    # or incomplete (False)
    p2_flag = True

    # look at each character
    for character in list(line.strip()):
        # if the character is an opening bracket
        if character in pairs.values():
            # put it in our temp list to create a list
            # of opening brackets
            temp_list.append(character)
        # if our list of opening brackets is empty OR if the bracket
        # has no match
        elif not temp_list or temp_list.pop() != pairs[character]:
            # print("corrupted line")
            # add to our points
            total_points_p1 += part1_points[character]

            # throw this line away, its corrupted instead of incomplete
            p2_flag = False
            break

    # if a line is incomplete then use it to calculate part 2
    if p2_flag:
        # print("incomplete line")
        # initialize that the total points for this line
        line_total = 0

        # flip the bracket order
        reversed_list = temp_list[::-1]

        # loop through the brackets
        for character in reversed_list:
            # calculate the points for this line
            line_total = 5 * line_total + part2_points[character]

        # append to our list for part 2
        list_points_p2.append(line_total)

# calculate the points for p2
total_points_p2 = sorted(list_points_p2)[len(list_points_p2) // 2]

print("part 1 solution:", total_points_p1)
print("part 2 solution:", total_points_p2)
