"""
Advent of Code 2024 Day 1: Historian Hysteria
https://adventofcode.com/2024/day/1
"""

from aocgen import get_user_input


def get_distance_sum(pairs: list[list[int]]) -> int:
    """Returns the sum of the distances between each selected pair in ``pairs``.

    Each pair in ``pairs`` is split into two lists. New pairs are made by popping
    the lowest value from each list and subtracting them to get a distance value.
    """
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
    """Gets the similarity score for each selected pair in ``pairs``.

    This score is calculated by splitting the pairs into two lists and adding the
    products of the items from the left list by the times they appear on the right.
    """
    left, right = [k for k in zip(*pairs)]

    return sum(item * right.count(item) for item in left)


if __name__ == "__main__":
    args = get_user_input(2024, 1)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    pair_list = [[int(n) for n in line.split()] for line in lines]

    if args["part"] == 1:
        print(f"Distance sum: {get_distance_sum(pair_list)}")
    elif args["part"] == 2:
        print(f"Similarity score: {get_similarity_score(pair_list)}")
