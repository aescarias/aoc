import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.readlines()

pair_list = [[int(n) for n in line.split()] for line in lines]

left, right = [list(enumerate(k)) for k in zip(*pair_list)]

distances = []

while len(left) or len(right):
    idx_a, a = min(left, key=lambda k: k[1])
    idx_b, b = min(right, key=lambda k: k[1])

    distances.append(abs(a - b))

    left.remove((idx_a, a))
    right.remove((idx_b, b))

print(sum(distances))
