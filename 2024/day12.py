"""
Advent of Code 2024 Day 12: Garden Groups
https://adventofcode.com/2024/day/12
"""

from collections import defaultdict
from itertools import product
from typing import NamedTuple

from aocgen import get_user_input
from aocutils import Point


class Bounds(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int


def get_adjacent_checked(
    position: Point, bounds: Bounds
) -> tuple[Point | None, Point | None, Point | None, Point | None]:
    """Returns the adjacent squares at ``position` that are within ``bounds``.

    The tuple returned is in the order of top, bottom, left, and right.
    """

    left = position + Point(-1, 0) if position.x - 1 >= bounds.left else None
    right = position + Point(1, 0) if position.x + 1 < bounds.right else None
    top = position + Point(0, -1) if position.y - 1 >= bounds.top else None
    bottom = position + Point(0, 1) if position.y + 1 < bounds.bottom else None

    return (top, bottom, left, right)


def get_adjacent_unchecked(position: Point) -> tuple[Point, Point, Point, Point]:
    """Returns the adjacent squares at ``position`` that may be present in a region.

    The tuple returned is in the order of top, bottom, left, and right.
    """

    left = position + Point(-1, 0)
    right = position + Point(1, 0)
    top = position + Point(0, -1)
    bottom = position + Point(0, 1)

    return (top, bottom, left, right)


def get_region_perimeter(region: set[Point]) -> int:
    """Returns the perimeter of a ``region`` of squares.

    The perimeter is determined by the amount of sides of a square that do not touch
    the sides of other neighbors.
    """

    return sum(
        4 - sum(adj in region for adj in get_adjacent_unchecked(point))
        for point in region
    )


def get_region_sides(region: set[Point]) -> int:
    """Returns the amount of bordering sides of a ``region`` of squares.

    The number of sides is determined by the amount of sides of a square that do not
    touch the sides of other neighbors and whose sides do not match with any of its
    adjacent squares.
    """

    sides = 0
    adjacent_squares = defaultdict[Point, list[Point | None]](list)

    for point in region:
        left, right, top, bottom = [
            adj if adj in region else None for adj in get_adjacent_unchecked(point)
        ]

        adjacent_squares[point] = [left, right, top, bottom]

        border_sides = sum(1 for side in adjacent_squares[point] if side is None)

        for side in adjacent_squares[point]:
            if side is not None:
                border_sides -= sum(
                    a is None and b is None
                    for a, b in zip(adjacent_squares[point], adjacent_squares[side])
                )

        sides += border_sides

    return sides


def explore_region(
    grid: list[list[str]], start: Point, seen: set[Point] | None = None
) -> set[Point]:
    """Explores a garden region starting at ``start`` and returns its plots.

    A garden region is comprised of plots growing the same type of plant. This
    function continuously searches for adjacent plots belonging to the region,
    skipping any ``seen`` points and stopping when no more can be found.

    When a region has been explored fully, the function returns the plots found.
    """

    width, height = len(grid[0]), len(grid)

    if seen is None:
        seen = set[Point]()

    plot_type = grid[start.y][start.x]
    region = {start}

    up, down, left, right = get_adjacent_checked(
        Point(start.x, start.y), Bounds(0, 0, width, height)
    )

    seen.add(start)

    for side in [up, down, left, right]:
        if side and side not in seen and grid[side.y][side.x] == plot_type:
            seen.add(side)
            region |= explore_region(grid, side, seen)

    return region


def get_garden_regions(grid: list[list[str]]) -> defaultdict[str, list[set[Point]]]:
    """Returns a mapping of plant types to garden regions in a grid.

    A garden region is a group of contiguous plots that grow the same type of plant.
    """

    width, height = len(grid[0]), len(grid)

    garden_regions = defaultdict[str, list[set[Point]]](list)
    seen_points = set[Point]()

    for y, x in product(range(height), range(width)):
        cell = grid[y][x]
        if Point(x, y) in seen_points:
            continue

        region = explore_region(grid, Point(x, y), seen_points)
        garden_regions[cell].append(region)

    return garden_regions


def get_garden_fence_price(
    regions: defaultdict[str, list[set[Point]]], discount: bool = False
) -> int:
    """Returns the cost of fencing all ``regions``.

    If ``discount`` is False, the price is calculated by multiplying the area of a region
    by its perimeter.

    If ``discount`` is True, the price is calculated by multiplying the area of a region
    by its amount of sides.

    Note: The area of a region is simply the amount of plots in it.
    """

    total_price = 0
    for plot_type in regions:
        for region in regions[plot_type]:
            area = len(region)

            if discount:
                sides = get_region_sides(region)

                total_price += area * sides
            else:
                perimeter = get_region_perimeter(region)

                total_price += area * perimeter

    return total_price


if __name__ == "__main__":
    args = get_user_input(2024, 12)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] in (1, 2):
        grid = [list(line) for line in lines]
        garden = get_garden_regions(grid)
        count = sum(len(regions) for regions in garden.values())

        if args["part"] == 1:
            cost = get_garden_fence_price(garden)

            print(f"The cost of fencing {count} regions is: {cost}")
        elif args["part"] == 2:
            cost = get_garden_fence_price(garden, discount=True)

            print(f"The cost of fencing {count} regions plus a discount is: {cost}")
