""" https://adventofcode.com/2024/day/2 """

raw_data = open("input.txt", 'r', encoding='utf-8').read().splitlines()

output = 0

for row in raw_data:
    temp_vals = list(map(int, row.split()))

    sub_val_bool = [False] * len(temp_vals)

    for index in range(len(temp_vals)):

        sub_val = temp_vals[:index] + temp_vals[index + 1:]

        diffs = [
            left_val - right_val for left_val, right_val
            in zip(sub_val, sub_val[1:])
        ]

        if(
            all(1 <= diff <= 3 for diff in diffs) or
            all(-1 >= diff >= -3 for diff in diffs)
        ):
            sub_val_bool[index] = True

    # print(sub_val_bool)
    if any(sub_val_bool):
        output += 1

print(output)
