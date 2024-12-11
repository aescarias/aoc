"""
Advent of Code 2024 Day 3: Mull It Over
https://adventofcode.com/2024/day/3
"""

import re

from aocfw import get_user_input


def sum_mul_operators(data: str, *, conditioned: bool) -> int:
    """Sums the multiplications included in ``data``.

    For a multiplication to be considered as such, it must be of the form ``mul(x,y)``
    where ``x`` and ``y`` are 1 to 3 length digits (although this length condition has not
    been observed in any of the inputs, it is still applied regardless).

    If ``conditioned`` is True, two new operators are considered: ``do()`` and ``don't()``.
    These effectively tell the interpreter when to consider multiplications.
    """
    mults = []
    can_multiply = True

    idx = 0
    while idx < len(data):
        if conditioned and (mat := re.match(r"don't\(\)", data[idx:])):
            can_multiply = False
            idx += mat.end()
        elif conditioned and (mat := re.match(r"do\(\)", data[idx:])):
            can_multiply = True
            idx += mat.end()
        elif can_multiply and (
            mat := re.match(r"mul\((\d{1,3}),(\d{1,3})\)", data[idx:])
        ):
            x, y = int(mat.group(1)), int(mat.group(2))
            mults.append(x * y)
            idx += mat.end()
        else:
            idx += 1

    return sum(mults)


if __name__ == "__main__":
    args = get_user_input(2024, 3)

    with args["input_file"] as fp:
        data = fp.read()

    if args["part"] == 1:
        print(f"Sum of multiplications: {sum_mul_operators(data, conditioned=False)}")
    elif args["part"] == 2:
        print(
            f"Sum of multiplications (conditioned): {sum_mul_operators(data, conditioned=True)}"
        )
