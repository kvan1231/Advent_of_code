""" https://adventofcode.com/2024/day/3 """

import re

raw_data = open("input.txt", 'r', encoding='utf-8').read()

mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
do_pattern = r"do\(\)|don't\(\)"

combined_pattern = f"{do_pattern}|{mul_pattern}"
matches = re.findall(combined_pattern, raw_data)

do_bool = True
output = 0

for match in matches:
    if match == "do()":
        do_bool = True
    elif match == "don't()":
        do_bool = False
    elif do_bool:
        x, y = map(int, match[4:-1].split(","))
        output += x * y

print(output)
