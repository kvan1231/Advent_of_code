""" https://adventofcode.com/2024/day/3 """

import re

raw_data = open("input.txt", 'r', encoding='utf-8').read()

pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, raw_data)
# print(matches)

products = [int(a) * int(b) for a, b in matches]

print(sum(products))