"""
Advent of Code 2024 Day 14: Restroom Redoubt
https://adventofcode.com/2024/day/14
"""

import re
from functools import reduce
from itertools import count
from typing import NamedTuple

from aocgen import get_user_input
from aocutils import Point, wrap_point


class Robot(NamedTuple):
    position: Point
    velocity: Point


def parse_robots(lines: list[str]) -> list[Robot]:
    """Parses and returns a list of robots in an area."""

    robots = []
    for line in lines:
        mat = re.match(
            r"p=(?P<rx>-?\d+),(?P<ry>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)", line
        )
        if not mat:
            continue

        robots.append(
            Robot(
                position=Point(x=int(mat.group("rx")), y=int(mat.group("ry"))),
                velocity=Point(x=int(mat.group("vx")), y=int(mat.group("vy"))),
            )
        )

    return robots


def step_robots(robots: list[Robot], width: int, height: int) -> None:
    """Moves robots in-place by one step."""

    for idx, robot in enumerate(robots):
        robots[idx] = Robot(
            wrap_point(robot.position + robot.velocity, (0, width), (0, height)),
            robot.velocity,
        )


def get_safety_factor(robots: list[Robot], width: int, height: int, steps: int) -> int:
    """Gets the safety factor for a group of ``robots`` given an area of ``width`` by
    ``height`` and moving the robots by an amount of ``steps``.

    The safety factor is the product of the amount of robots in each quadrant.
    """

    for _ in range(steps):
        step_robots(robots, width, height)

    # quadrants normalized so up means negative and down means positive
    quadrants = {"+x-y": [], "-x-y": [], "-x+y": [], "+x+y": []}
    x_axis = width // 2
    y_axis = height // 2

    for robot in robots:
        pos = robot.position

        if pos.x > x_axis and pos.y < y_axis:
            quadrants["+x-y"].append(robot)
        elif pos.x < x_axis and pos.y < y_axis:
            quadrants["-x-y"].append(robot)
        elif pos.x < x_axis and pos.y > y_axis:
            quadrants["-x+y"].append(robot)
        elif pos.x > x_axis and pos.y > y_axis:
            quadrants["+x+y"].append(robot)

    return reduce(lambda x, y: x * y, [len(quad) for quad in quadrants.values()])


def find_earliest_tree(robots: list[Robot], width: int, height: int) -> int:
    """Finds the earliest 'Christmas Tree' picture formed by ``robots`` and in an
    area of ``width`` by ``height``.

    It is assumed that a picture is formed if a row of robots longer than 7 is found.
    """

    for loop in count(1):
        grid = [list("." * width) for _ in range(height)]
        step_robots(robots, width, height)
        for robot in robots:
            grid[robot.position.y][robot.position.x] = "#"

        for robot in robots:
            if "".join(grid[robot.position.y][robot.position.x :]).startswith("#" * 8):
                return loop

    return -1  # this won't be reached, but pyright complains anyways


if __name__ == "__main__":
    args = get_user_input(2024, 14)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    print("Leave the following fields empty to use defaults.")
    width = input("Width: ").strip()
    height = input("Height: ").strip()
    steps = input("Steps (part 1 only): ").strip()

    width = int(width) if width else 101
    height = int(height) if height else 103
    steps = int(steps) if steps else 100

    if args["part"] == 1:
        robots = parse_robots(lines)

        factor = get_safety_factor(robots, width, height, steps)
        print(f"The safety factor after {steps} step(s) is {factor}")
    elif args["part"] == 2:
        robots = parse_robots(lines)

        tree_steps = find_earliest_tree(robots, width, height)
        print(f"The earliest christmas tree can be found in {tree_steps} step(s).")
