""" https://adventofcode.com/2024/day/1 """

first_list = []
second_list = []

raw_data = open("input.txt").read().splitlines()

for line in raw_data:
    val_a, val_b = list(map(int, line.split()))

    first_list.append(val_a)
    second_list.append(val_b)

output = 0

for value in first_list:
    output += value * second_list.count(value)
print(output)
