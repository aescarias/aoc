"""
Advent of Code 2024 Day 7: Bridge Repair
https://adventofcode.com/2024/day/7
"""

from dataclasses import dataclass

from aocfw import get_user_input


@dataclass
class Tree:
    operands: list[int]
    target: int
    concat: bool = False
    visited: bool = False

    def visit(self) -> tuple["Tree | None", "Tree | None", "Tree | None"]:
        left = self.operands.pop(0)
        right = self.operands.pop(0)

        mult = left * right
        added = left + right
        concat = int(str(left) + str(right))

        if mult <= self.target:
            mult_tree = Tree([mult, *self.operands], self.target, self.concat)
        else:
            mult_tree = None

        if added <= self.target:
            added_tree = Tree([added, *self.operands], self.target, self.concat)
        else:
            added_tree = None

        if self.concat and concat <= self.target:
            concat_tree = Tree([concat, *self.operands], self.target, self.concat)
        else:
            concat_tree = None

        self.visited = True
        return (added_tree, mult_tree, concat_tree)

    @property
    def solved(self) -> bool:
        return len(self.operands) == 1 and self.operands[0] == self.target

    @property
    def can_visit(self) -> bool:
        return len(self.operands) >= 2


def tree_has_solutions(tree: Tree) -> bool:
    branches: list[Tree] = [tree]
    solved: list[Tree] = []

    while branches:
        branch = branches.pop()

        if not branch.can_visit:
            if branch.solved:
                solved.append(branch)
                continue

            if len(branch.operands) == 1:
                continue

        splits = branch.visit()

        for sp in splits:
            if sp is not None:
                branches.append(sp)

    return bool(solved)


def sum_calibration_results(lines: list[str], *, concat: bool) -> int:
    true_sum = 0

    for line in lines:
        total, operands = line.split(":")

        total = int(total)
        operands = [int(item) for item in operands.split()]

        splits = Tree(operands, total, concat).visit()

        if any(tree_has_solutions(sp) if sp is not None else False for sp in splits):
            true_sum += total

    return true_sum


if __name__ == "__main__":
    args = get_user_input(2024, 7)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        result = sum_calibration_results(lines, concat=False)
        print(f"Total calibration result: {result}")
    elif args["part"] == 2:
        result = sum_calibration_results(lines, concat=True)
        print(f"Total calibration result (with concat operator): {result}")
