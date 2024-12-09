import sys
from collections import defaultdict
from itertools import product
from typing import NamedTuple

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()


class Point(NamedTuple):
    x: int
    y: int


ANGLES = ["^", ">", "v", "<"]


def get_moved_positions(grid: list[list[str]]) -> tuple[defaultdict[Point, int], bool]:
    width, height = len(grid[0]), len(grid)

    guard_pos = Point(-1, -1)

    for y, x in product(range(height), range(width)):
        cell = grid[y][x]

        if cell in ANGLES:
            guard_pos = Point(x, y)
            break

    visited = defaultdict[Point, int](int)

    while True:
        current = grid[guard_pos.y][guard_pos.x]
        visited[guard_pos] += 1

        if visited[guard_pos] >= 4:
            return (visited, True)

        if (guard_pos.x + 1) < width:
            right = grid[guard_pos.y][guard_pos.x + 1]
        else:
            right = None

        if (guard_pos.x - 1) >= 0:
            left = grid[guard_pos.y][guard_pos.x - 1]
        else:
            left = None

        if (guard_pos.y + 1) < height:
            down = grid[guard_pos.y + 1][guard_pos.x]
        else:
            down = None

        if (guard_pos.y - 1) >= 0:
            up = grid[guard_pos.y - 1][guard_pos.x]
        else:
            up = None

        if current == "^":
            if up is None:
                break

            if up in ("#", "O"):
                grid[guard_pos.y][guard_pos.x] = ">"
            else:
                grid[guard_pos.y - 1][guard_pos.x] = "^"
                grid[guard_pos.y][guard_pos.x] = "X"
                guard_pos = Point(guard_pos.x, guard_pos.y - 1)
        elif current == ">":
            if right is None:
                break

            if right in ("#", "O"):
                grid[guard_pos.y][guard_pos.x] = "v"
            else:
                grid[guard_pos.y][guard_pos.x + 1] = ">"
                grid[guard_pos.y][guard_pos.x] = "X"
                guard_pos = Point(guard_pos.x + 1, guard_pos.y)
        elif current == "v":
            if down is None:
                break

            if down in ("#", "O"):
                grid[guard_pos.y][guard_pos.x] = "<"
            else:
                grid[guard_pos.y + 1][guard_pos.x] = "v"
                grid[guard_pos.y][guard_pos.x] = "X"
                guard_pos = Point(guard_pos.x, guard_pos.y + 1)

        elif current == "<":
            if left is None:
                break

            if left in ("#", "O"):
                grid[guard_pos.y][guard_pos.x] = "^"
            else:
                grid[guard_pos.y][guard_pos.x - 1] = "<"
                grid[guard_pos.y][guard_pos.x] = "X"
                guard_pos = Point(guard_pos.x - 1, guard_pos.y)

    return (visited, False)


grid = [list(line) for line in lines]
width, height = len(grid[0]), len(grid)

loops = 0

possible_positions, loop = get_moved_positions(grid)

# let's hope grid isn't already a loop situation
assert not loop

print(f"Will visit {len(possible_positions)} positions.")


def produces_loop(lines: list[str], point: Point) -> bool:
    grid = [list(line) for line in lines]

    if grid[point.y][point.x] in ANGLES:
        return False

    grid[point.y][point.x] = "O"

    _, loop = get_moved_positions(grid)
    if loop:
        return True

    grid[point.y][point.x] = "."

    return False


if __name__ == "__main__":
    print(sum(produces_loop(lines, point) for point in possible_positions))
