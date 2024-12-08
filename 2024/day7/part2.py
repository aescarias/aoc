import sys
from dataclasses import dataclass

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()


@dataclass
class Tree:
    operands: list[int]
    target: int
    visited: bool = False

    def visit(self) -> tuple["Tree | None", "Tree | None", "Tree | None"]:
        left = self.operands.pop(0)
        right = self.operands.pop(0)

        mult = left * right
        added = left + right
        concat = int(str(left) + str(right))

        if mult <= self.target:
            mult_tree = Tree([mult, *self.operands], self.target)
        else:
            mult_tree = None

        if added <= self.target:
            added_tree = Tree([added, *self.operands], self.target)
        else:
            added_tree = None

        if concat <= self.target:
            concat_tree = Tree([concat, *self.operands], self.target)
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


def explore_branch(tree: Tree) -> bool:
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

        left, middle, right = branch.visit()

        if left is not None:
            branches.append(left)
        if middle is not None:
            branches.append(middle)
        if right is not None:
            branches.append(right)

    return bool(solved)


true_sum = 0

for line in lines:
    total, operands = line.split(":")

    total = int(total)
    operands = [int(item) for item in operands.split()]

    a, b, c = Tree(operands, total).visit()

    a_solved = explore_branch(a) if a is not None else False
    b_solved = explore_branch(b) if b is not None else False
    c_solved = explore_branch(c) if c is not None else False

    if a_solved or b_solved or c_solved:
        true_sum += total

print(true_sum)
