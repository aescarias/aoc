import re
import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.readlines()

mults = []

can_multiply = True

for line in lines:
    idx = 0

    while idx < len(line):
        if mat := re.match(r"don't\(\)", line[idx:]):
            can_multiply = False
            idx += mat.end()
        elif mat := re.match(r"do\(\)", line[idx:]):
            can_multiply = True
            idx += mat.end()
        elif can_multiply and (
            mat := re.match(r"mul\((\d{1,3}),(\d{1,3})\)", line[idx:])
        ):
            x, y = int(mat.group(1)), int(mat.group(2))
            mults.append(x * y)
            idx += mat.end()
        else:
            idx += 1

print(sum(mults))
