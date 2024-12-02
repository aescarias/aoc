import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.readlines()

level_groups = [[int(n) for n in line.split()] for line in lines]


def is_group_safe(group: list[int]) -> bool:
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


safe_groups = 0
for group in level_groups:
    if is_group_safe(group):
        safe_groups += 1
        continue

    # The Problem Dampener extension
    # Make things safe if removing a level makes it safe.
    for idx in range(len(group)):
        group_copy = group.copy()
        group_copy.pop(idx)

        if is_group_safe(group_copy):
            safe_groups += 1
            break


print(safe_groups)
