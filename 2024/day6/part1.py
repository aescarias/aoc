import sys
from dataclasses import dataclass

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()


@dataclass
class Point:
    x: int
    y: int


ANGLES = ["^", ">", "v", "<"]
OBSTACLE = "#"

grid = [list(line) for line in lines]
width, height = len(grid[0]), len(grid)

guard_pos = Point(-1, -1)

for y in range(height):
    for x in range(width):
        cell = grid[y][x]

        if cell in ANGLES:
            guard_pos = Point(x, y)
            break

while True:
    current = grid[guard_pos.y][guard_pos.x]
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

        if up == "#":
            grid[guard_pos.y][guard_pos.x] = ">"
        else:
            grid[guard_pos.y - 1][guard_pos.x] = "^"
            grid[guard_pos.y][guard_pos.x] = "X"
            guard_pos.y -= 1
    elif current == ">":
        if right is None:
            break

        if right == "#":
            grid[guard_pos.y][guard_pos.x] = "v"
        else:
            grid[guard_pos.y][guard_pos.x + 1] = ">"
            grid[guard_pos.y][guard_pos.x] = "X"
            guard_pos.x += 1
    elif current == "v":
        if down is None:
            break

        if down == "#":
            grid[guard_pos.y][guard_pos.x] = "<"
        else:
            grid[guard_pos.y + 1][guard_pos.x] = "v"
            grid[guard_pos.y][guard_pos.x] = "X"
            guard_pos.y += 1
    elif current == "<":
        if left is None:
            break

        if left == "#":
            grid[guard_pos.y][guard_pos.x] = "^"
        else:
            grid[guard_pos.y][guard_pos.x - 1] = "<"
            grid[guard_pos.y][guard_pos.x] = "X"
            guard_pos.x -= 1

print(sum(line.count("X") for line in grid) + 1)
