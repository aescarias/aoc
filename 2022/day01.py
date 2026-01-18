"""
Advent of Code 2022 Day 1: Calorie Counting
https://adventofcode.com/2022/day/1
"""

from aocgen import get_user_input


def group_number_lines(lines: list[str]) -> list[list[int]]:
    num_groups: list[list[int]] = []
    current_group: list[int] = []

    for line in lines:
        line = line.strip()
        if not line:
            num_groups.append(current_group)
            current_group = []
            continue

        current_group.append(int(line))

    if current_group:
        num_groups.append(current_group)

    return num_groups


if __name__ == "__main__":
    args = get_user_input(2022, 1)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        fruit_groups = group_number_lines(lines)
        max_calories = max(sum(fruits) for fruits in fruit_groups)
        print(f"Elf carrying the most calories has {max_calories}.")
    elif args["part"] == 2:
        fruit_groups = group_number_lines(lines)
        max_calorie_rank = sorted(
            (sum(fruits) for fruits in fruit_groups), reverse=True
        )
        sum_of_three = sum(max_calorie_rank[:3])
        print(f"The 3 elves carrying the most calories have {sum_of_three}.")
