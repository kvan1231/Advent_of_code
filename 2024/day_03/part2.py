""" https://adventofcode.com/2024/day/3 """

import re

raw_data = open("input.txt", 'r', encoding='utf-8').read()

ignored_pattern = r"don't\(\).*?do\(\)"
cleaned_string = re.sub(ignored_pattern, "", raw_data)

pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, cleaned_string)
# print(matches)

products = [int(a) * int(b) for a, b in matches]

print(sum(products))