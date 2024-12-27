from __future__ import annotations

from dataclasses import dataclass


def wrap(value: int, minimum: int, maximum: int) -> int:
    """Returns a value such that ``minimum <= value < maximum``, wrapping if necessary."""
    if minimum <= value < maximum:
        return value

    return minimum + (value - minimum) % (maximum - minimum)


def wrap_point(point: Point, xval: tuple[int, int], yval: tuple[int, int]) -> Point:
    """Returns a point such that ``xmin <= x < xmax`` and ``ymin <= y < ymax``,
    wrapping if necessary."""
    return Point(wrap(point.x, *xval), wrap(point.y, *yval))


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


class Cell:
    def __init__(self, grid: Grid, point: Point) -> None:
        self.grid = grid
        self.point = point

    def __str__(self) -> str:
        return self.grid.space[self.point.y][self.point.x]

    def _bound_move(self, dx: int, dy: int) -> Cell | None:
        new_position = self.point + Point(dx, dy)
        if self.grid.is_valid(new_position):
            return Cell(self.grid, new_position)

    @property
    def left(self) -> Cell | None:
        return self._bound_move(-1, 0)

    @property
    def right(self) -> Cell | None:
        return self._bound_move(1, 0)

    @property
    def top(self) -> Cell | None:
        return self._bound_move(0, -1)

    @property
    def bottom(self) -> Cell | None:
        return self._bound_move(0, 1)

    @property
    def top_left(self) -> Cell | None:
        return self._bound_move(-1, -1)

    @property
    def top_right(self) -> Cell | None:
        return self._bound_move(1, -1)

    @property
    def bottom_left(self) -> Cell | None:
        return self._bound_move(-1, 1)

    @property
    def bottom_right(self) -> Cell | None:
        return self._bound_move(1, 1)


class Grid:
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        self.space = [list(" " * width) for _ in range(height)]

    @property
    def width(self) -> int:
        return len(self.space[0])

    @property
    def height(self) -> int:
        return len(self.space)

    def at(self, point: Point) -> Cell:
        return Cell(self, point)

    def put(self, point: Point, value: str) -> None:
        self.space[point.y][point.x] = value

    def is_valid(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height
