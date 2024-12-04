""" https://adventofcode.com/2024/day/2 """

raw_data = open("input.txt", 'r', encoding='utf-8').read().splitlines()

output = 0

for row in raw_data:
    temp_vals = list(map(int, row.split()))
    diffs = [
        left_val - right_val for left_val, right_val
        in zip(temp_vals, temp_vals[1:])
    ]
    # print(diffs)

    if (
        all(1 <= diff <= 3 for diff in diffs) or
        all(-1 >= diff >= -3 for diff in diffs)
    ):
        output += 1

print(output)