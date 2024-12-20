""" https://adventofcode.com/2024/day/4 """

def find_xmas(grid: list) -> int:
    """Finds the word `XMAS` in an inputted grid that is represented
    as a list of strings

    Parameters
    ----------
    grid : list
        The input grid consisting of a list of strings

    Returns
    -------
    int
        The count of the number of times the word XMAS appears
    """
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, -1), # Up-Left
        (-1, 1),  # Up-Right
        (1, -1),  # Down-Left
        (1, 1),   # Down-Right
    ]

    def _is_valid(x: int, y: int) -> bool:
        """A boolean check if the direction moved is valid and remains in
        the grid

        Parameters
        ----------
        x : int
            The row index we're validating
        y : int
            The column index we're validating

        Returns
        -------
        bool
            the validity of the position
        """

        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def _word_exists(x: int, y: int, dx: int, dy: int) -> bool:
        """Determines if XMAS exists from a start point (x, y) to an
        end point (x +- dx, y +- dy)

        Parameters
        ----------
        x : int
            Initial starting row
        y : int
            Initial starting column
        dx : int
            Direction we want to search in
        dy : int
            Direction we want to search in

        Returns
        -------
        bool
            True if the word XMAS is found, False otherwise
        """

        word = 'XMAS'

        for nchar, char in enumerate(word):
            nx, ny = x + nchar * dx, y + nchar * dy
            if not _is_valid(nx, ny) or grid[nx][ny] != char:
                return False
        return True

    found_xmas = []

    for rind, row in enumerate(grid):
        for cind, character in enumerate(row):
            if character == 'X':
                for dx, dy in directions:
                    if _word_exists(rind, cind, dx, dy):
                        found_xmas.append((rind, cind, dx, dy))

    return found_xmas

raw_data = open("input.txt", 'r', encoding='utf-8').read().splitlines()

xmas_grid = [list(row) for row in raw_data]

results = find_xmas(xmas_grid)

print(len(results))
