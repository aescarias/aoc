"""
Advent of Code 2024 Day 6: Guard Gallivant
https://adventofcode.com/2024/day/6
"""

from collections import defaultdict
from itertools import product
from typing import NamedTuple

from aocfw import get_user_input


class Point(NamedTuple):
    x: int
    y: int

    def moved(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)


DIRECTIONS = {
    "^": {"turn": ">", "move": (0, -1)},
    ">": {"turn": "v", "move": (1, 0)},
    "v": {"turn": "<", "move": (0, 1)},
    "<": {"turn": "^", "move": (-1, 0)},
}

OBSTACLE = "#"
VISITED = "X"


class GuardMap:
    """A grid of NxM length indicating the guard's map."""

    def __init__(self, cells: list[list[str]]) -> None:
        """
        Arguments:
            cells (list[list[str]]):
                A list of rows representing the grid.

        """
        self.cells = cells
        self.width = len(self.cells[0])
        self.height = len(self.cells)

        self.position = self._find_guard_position()
        self.visited = defaultdict[Point, int](int)

    def _find_guard_position(self) -> Point:
        for y, x in product(range(self.height), range(self.width)):
            if self.cells[y][x] in DIRECTIONS:
                return Point(x, y)

        raise ValueError("No guard found in map.")

    @property
    def current(self) -> str:
        return self.cells[self.position.y][self.position.x]

    @current.setter
    def current(self, value: str) -> None:
        self.cells[self.position.y][self.position.x] = value

    def cell_at(self, point: Point) -> str:
        return self.cells[point.y][point.x]

    def in_map(self, point: Point) -> bool:
        return 0 <= point.y < self.height and 0 <= point.x < self.width

    def step(self) -> bool:
        symbol = self.current
        direction = DIRECTIONS[symbol]

        next_pos = self.position.moved(*direction["move"])
        if not self.in_map(next_pos):
            self.visited[self.position] += 1
            self.current = VISITED
            return False

        if self.cell_at(next_pos) == OBSTACLE:
            self.current = direction["turn"]
        else:
            self.visited[self.position] += 1
            self.current = VISITED
            self.position = next_pos
            self.current = symbol

        return True

    def run(self) -> bool:
        while self.step():
            if self.visited[self.position] >= 4:
                return True

        return False
        # print(*["".join(line) for line in self.cells], sep="\n")
        # __import__("time").sleep(1)
        # print("\x1b[2J")


def visit_positions(lines: list[str]) -> int:
    guard_map = GuardMap([list(line) for line in lines])
    guard_map.run()

    return len(guard_map.visited)


def get_possible_loops(lines: list[str]) -> int:
    initial_map = GuardMap([list(line) for line in lines])
    initial_map.run()

    loops = 0
    for point in initial_map.visited:
        checked_map = GuardMap([list(line) for line in lines])
        if checked_map.cells[point.y][point.x] in DIRECTIONS:
            continue

        checked_map.cells[point.y][point.x] = OBSTACLE
        looped = checked_map.run()
        if looped:
            loops += 1

    return loops


if __name__ == "__main__":
    args = get_user_input(2024, 6)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        print(f"Visited positions: {visit_positions(lines)}")
    elif args["part"] == 2:
        print(f"Loops possible: {get_possible_loops(lines)}")
