"""
Advent of Code 2024 Day 13: Claw Contraption
https://adventofcode.com/2024/day/13
"""

import re
from collections.abc import Generator
from typing import NamedTuple

from aocgen import get_user_input


class Point(NamedTuple):
    x: int
    y: int

    def moved(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)


class ClawMachine(NamedTuple):
    button_a: Point
    button_b: Point
    prize: Point


def get_button_a_presses(machine: ClawMachine) -> float:
    """Returns the presses needed for button A so it can reach the prize."""

    # A=\frac{-Xy_2+Yx_2}{-x_1y_2+y_1x_2}
    return (
        -machine.prize.x * machine.button_b.y + machine.prize.y * machine.button_b.x
    ) / (
        -machine.button_a.x * machine.button_b.y
        + machine.button_a.y * machine.button_b.x
    )


def get_button_b_presses(machine: ClawMachine) -> float:
    """Returns the presses needed for button A so it can reach the prize."""

    # B=\frac{-Xy_1+Yx_1}{-y_1x_2+x_1y_2}
    return (
        -machine.button_a.y * machine.prize.x + machine.button_a.x * machine.prize.y
    ) / (
        -machine.button_a.y * machine.button_b.x
        + machine.button_b.y * machine.button_a.x
    )


def get_button_presses(machine: ClawMachine) -> tuple[int | None, int | None]:
    """Returns the button presses needed to reach the prize.

    Returns a tuple of two entries representing the times button A and button B must
    be pressed respectively. If both items are None, it means that the prize is unreachable
    no matter the amount of presses
    """

    b_presses = get_button_b_presses(machine)
    a_presses = get_button_a_presses(machine)

    if a_presses.is_integer() and b_presses.is_integer():
        return (int(a_presses), int(b_presses))

    return (None, None)


def match_to_point(mat: re.Match) -> Point:
    """Converts a regex match with groups 'x' and 'y' to a point."""
    return Point(int(mat.group("x")), int(mat.group("y")))


def parse_claw_machines(
    lines: list[str], prize_increment: int = 0
) -> Generator[ClawMachine, None, None]:
    """Parses and yields the claw machines in ``lines``.

    If ``prize_increment`` is provided, the prize's X and Y is increased by it (this is
    to account for part 2).
    """
    lines = [line for line in lines if line.strip()]

    for idx in range(0, len(lines), 3):
        batch = lines[idx : idx + 3]

        btn_a_match = re.match(r"Button A: X\+(?P<x>\d+), Y\+(?P<y>\d+)", batch[0])
        btn_b_match = re.match(r"Button B: X\+(?P<x>\d+), Y\+(?P<y>\d+)", batch[1])
        prize_match = re.match(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)", batch[2])

        if btn_a_match and btn_b_match and prize_match:
            yield ClawMachine(
                match_to_point(btn_a_match),
                match_to_point(btn_b_match),
                match_to_point(prize_match).moved(prize_increment, prize_increment),
            )


A_TOKENS, B_TOKENS = 3, 1


def get_required_tokens(machine: ClawMachine) -> int | None:
    """Gets the amount of tokens needed to get the prize.

    If the prize is unreachable no matter the amount of tokens, returns None.
    """
    a_presses, b_presses = get_button_presses(machine)

    if a_presses is not None and b_presses is not None:
        return (a_presses * A_TOKENS) + (b_presses * B_TOKENS)


if __name__ == "__main__":
    args = get_user_input(2024, 13)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        tokens = sum(
            tok
            for machine in parse_claw_machines(lines)
            if (tok := get_required_tokens(machine)) is not None
        )

        print(
            f"Tokens needed to get the prizes from all solvable claw machines: {tokens}"
        )
    elif args["part"] == 2:
        tokens = sum(
            tok
            for machine in parse_claw_machines(lines, 10_000_000_000_000)
            if (tok := get_required_tokens(machine)) is not None
        )

        print(
            f"Tokens needed to get the prizes from all solvable claw machines (plus the offset): {tokens}"
        )
