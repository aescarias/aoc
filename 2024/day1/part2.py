import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.readlines()

pair_list = [[int(n) for n in line.split()] for line in lines]

left, right = [k for k in zip(*pair_list)]

similarity_scores = []

for item in left:
    similarity_scores.append(item * right.count(item))

print(sum(similarity_scores))
