import re
import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.readlines()

mults = []

for line in lines:
    for mat in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line):
        x, y = int(mat.group(1)), int(mat.group(2))
        mults.append(x * y)

print(sum(mults))
