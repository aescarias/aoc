"""
Advent of Code 2024 Day 4: Ceres Search
https://adventofcode.com/2024/day/4
"""

from itertools import product

from aocgen import get_user_input


class Grid:
    """A grid of NxM length."""

    def __init__(self, cells: list[str]) -> None:
        """
        Arguments:
            cells (list[str]):
                A list of rows representing the grid.
        """
        self.cells = cells
        self.width = len(self.cells[0])
        self.height = len(self.cells)

    def matches_horizontally(self, x: int, y: int, targets: tuple[str, ...]) -> bool:
        """Returns whether any of ``targets`` matches horizontally from position (x, y)."""
        return y < self.height and self.cells[y][x:].startswith(targets)

    def matches_vertically(self, x: int, y: int, targets: tuple[str, ...]) -> bool:
        """Returns whether any of ``targets`` matches vertically from position (x, y)."""
        return "".join(
            row[x : x + 1] for row in self.cells[y : y + len(max(targets, key=len))]
        ).startswith(targets)

    def matches_diagonally(
        self, x: int, y: int, targets: tuple[str, ...]
    ) -> tuple[bool, bool]:
        """Checks whether any of ``targets`` matches diagonally from position (x, y).

        Returns a tuple of two booleans - the first being if a diagonal match was found
        and the second being if an anti-diagonal match was found.
        """
        length = len(max(targets, key=len))

        if y + length > self.height:
            return (False, False)

        diagonal = "".join(
            self.cells[y + inc][x + inc : x + inc + 1] for inc in range(length)
        )

        antidiagonal = "".join(
            self.cells[y + dy][x + dx - 1 : x + dx]
            for dy, dx in zip(range(length), range(length, 0, -1))
        )

        return (diagonal.startswith(targets), antidiagonal.startswith(targets))


def get_word_frequency(lines: list[str], targets: tuple[str, ...]) -> int:
    """Searches ``targets`` in ``lines``. A target will be considered found if it appears
    horizontally, vertically, diagonally or anti-diagonally at any point in the grid."""
    grid = Grid(lines)

    word_count = 0

    for y, x in product(range(grid.height), range(grid.width)):
        word_count += sum(
            (
                grid.matches_horizontally(x, y, targets),
                grid.matches_vertically(x, y, targets),
                *grid.matches_diagonally(x, y, targets),
            )
        )

    return word_count


def get_cross_frequency(lines: list[str], targets: tuple[str, ...]) -> int:
    """Searches ``targets`` in ``lines``. A target will be considered found if it appears
    both diagonally and anti-diagonally (forming a cross) at any point in the grid."""
    grid = Grid(lines)

    word_count = 0

    for y, x in product(range(grid.height), range(grid.width)):
        diag, antidiag = grid.matches_diagonally(x, y, targets)
        if diag and antidiag:
            word_count += 1

    return word_count


if __name__ == "__main__":
    args = get_user_input(2024, 4)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    first_targets = ("XMAS", "SAMX")
    second_targets = ("MAS", "SAM")

    if args["part"] == 1:
        print(
            f"Times {first_targets} appear in input: {get_word_frequency(lines, first_targets)}"
        )
    elif args["part"] == 2:
        print(
            f"Times {second_targets} appear in input as crosses: {get_cross_frequency(lines, second_targets)}"
        )
