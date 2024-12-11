"""
Advent of Code 2024 Day 2: Red-Nosed Reports
https://adventofcode.com/2024/day/2
"""

from aocfw import get_user_input


def is_group_safe(group: list[int]) -> bool:
    """Determines whether a group can be considered safe.

    A group is considered safe as is if the following conditions are met:
    - Each of its levels increase or decrease, but not both.
    - The distance between two levels is at least 1 and at most 3.
    """
    diff = group[0]
    tendency = None

    for level in group[1:]:
        if tendency is None:
            if level > diff:
                tendency = "I"
            elif level < diff:
                tendency = "D"

        if level == diff:
            return False

        if abs(level - diff) > 3:
            return False

        if level > diff and tendency == "D":
            return False
        elif level < diff and tendency == "I":
            return False

        diff = level

    return True


def is_dampened_group_safe(group: list[int]) -> bool:
    """Determines whether a group can be considered safe if dampening is applied.

    Alongside the conditions for a traditional safe group, a group is considered dampened
    if it was made safe by removing one of its levels.
    """
    if is_group_safe(group):
        return True

    for idx in range(len(group)):
        group_copy = group.copy()
        group_copy.pop(idx)

        if is_group_safe(group_copy):
            return True

    return False


def get_safe_group_count(groups: list[list[int]]) -> int:
    """Returns the amount of safe groups in ``groups``."""
    return sum(is_group_safe(group) for group in groups)


def get_dampened_group_count(groups: list[list[int]]) -> int:
    """Returns the amount of safe groups in ``groups`` but also applying dampening if necessary."""
    return sum(is_dampened_group_safe(group) for group in groups)


if __name__ == "__main__":
    args = get_user_input(2024, 2)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    level_groups = [[int(n) for n in line.split()] for line in lines]

    if args["part"] == 1:
        print(f"Safe groups: {get_safe_group_count(level_groups)}")
    elif args["part"] == 2:
        print(f"Safe groups (with dampening): {get_dampened_group_count(level_groups)}")
