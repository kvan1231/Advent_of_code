""" https://adventofcode.com/2024/day/1 """

first_list = []
second_list = []

raw_data = open("input.txt").read().splitlines()

for line in raw_data:
    val_a, val_b = list(map(int, line.split()))

    first_list.append(val_a)
    second_list.append(val_b)

first_list.sort()
second_list.sort()

output = 0

for index in range(len(first_list)):
    output += abs(first_list[index] - second_list[index])

print(output)
