"""
Advent of Code 2024 Day 1: Historian Hysteria
https://adventofcode.com/2024/day/1
"""

from aocgen import get_user_input


def get_total_distance(pairs: list[list[int]]) -> int:
    left, right = [list(enumerate(k)) for k in zip(*pairs)]

    distances = []

    while len(left) or len(right):
        idx_a, a = min(left, key=lambda k: k[1])
        idx_b, b = min(right, key=lambda k: k[1])

        distances.append(abs(a - b))

        left.remove((idx_a, a))
        right.remove((idx_b, b))

    return sum(distances)


def get_similarity_score(pairs: list[list[int]]) -> int:
    left, right = [k for k in zip(*pairs)]

    return sum(item * right.count(item) for item in left)


if __name__ == "__main__":
    args = get_user_input(2024, 1)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    pair_list = [[int(n) for n in line.split()] for line in lines]

    if args["part"] == 1:
        print(f"Total distance: {get_total_distance(pair_list)}")
    elif args["part"] == 2:
        print(f"Similarity score: {get_similarity_score(pair_list)}")
