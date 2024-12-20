""" https://adventofcode.com/2024/day/4 """

def find_x_pattern(grid: list) -> tuple[int, list]:
    """Finds the number of "MAS" X patterns in the input grid and their locations.

    A "MAS" X pattern consists of:
    - An "A" at the center.
    - "M" and "S" in opposite diagonal corners.

    Parameters
    ----------
    grid : list
        The input grid consisting of a list of strings.

    Returns
    -------
    tuple[int, list]
        A tuple containing the count of "MAS" X patterns found and a list of their
        center coordinates.
    """
    count = 0
    patterns = []

    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            if grid[row][col] != "A":
                continue
            corners = [
                grid[row - 1][col - 1], grid[row - 1][col + 1],
                grid[row + 1][col + 1], grid[row + 1][col - 1]
            ]
            if "".join(corners) in ["MMSS", "MSSM", "SSMM", "SMMS"]:
                count += 1
                patterns.append((row, col))

    return count, patterns

raw_data = open("input.txt", 'r', encoding='utf-8').read().splitlines()

# Convert input grid to a list of lists for easier processing
xmas_grid = [list(row) for row in raw_data]

# Find X patterns
x_count, x_patterns = find_x_pattern(xmas_grid)

# Print the count and results
print(f"Total X patterns found: {x_count}")
