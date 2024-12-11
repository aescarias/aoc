"""
Advent of Code 2024 Day 5: Print Queue
https://adventofcode.com/2024/day/5
"""

from itertools import pairwise
from typing import NamedTuple

from aocfw import get_user_input


class OrderRule(NamedTuple):
    before: int
    after: int


class PrintQueue(NamedTuple):
    ordering_rules: list[OrderRule]
    updates: list[list[int]]


def parse_print_queue(lines: list[str]) -> PrintQueue:
    page_ordering_rules: list[OrderRule] = []
    updates: list[list[int]] = []

    current_section = "page-order"
    for line in lines:
        if not line:
            current_section = "updates"
            continue

        if current_section == "page-order":
            before, after = list(int(val) for val in line.split("|"))
            page_ordering_rules.append(OrderRule(before, after))
        else:
            pages = list(int(val) for val in line.split(","))
            updates.append(pages)

    return PrintQueue(page_ordering_rules, updates)


def is_ordered(update: list[int], ordering_rules: list[OrderRule]) -> bool:
    for current_page, next_page in pairwise(update):
        page_order = next(
            item
            for item in ordering_rules
            if current_page in item and next_page in item
        )
        if (current_page, next_page) != page_order:
            return False

    return True


def order_update(update: list[int], ordering_rules: list[OrderRule]) -> list[int]:
    """Orders ``update`` according to ``ordering_rules``.

    Note: ``order_update`` assumes that the values in ``update`` are unique.
    """

    page_orders = [
        item
        for item in ordering_rules
        if item.before in update and item.after in update
    ]

    sorted_update = update.copy()

    while not is_ordered(sorted_update, page_orders):
        for before, after in page_orders:
            idx_before = sorted_update.index(before)
            idx_after = sorted_update.index(after)

            if idx_before > idx_after:
                sorted_update[idx_before], sorted_update[idx_after] = (
                    sorted_update[idx_after],
                    sorted_update[idx_before],
                )

    return sorted_update


def get_correct_middle_update_sum(queue: PrintQueue) -> int:
    middle_page_sum = 0

    for update in queue.updates:
        if is_ordered(update, queue.ordering_rules):
            middle_page_sum += update[len(update) // 2]

    return middle_page_sum


def get_incorrect_middle_update_sum(queue: PrintQueue) -> int:
    middle_page_sum = 0

    for update in queue.updates:
        if not is_ordered(update, queue.ordering_rules):
            ordered = order_update(update, queue.ordering_rules)
            middle_page_sum += ordered[len(ordered) // 2]

    return middle_page_sum


if __name__ == "__main__":
    args = get_user_input(2024, 5)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    queue = parse_print_queue(lines)

    if args["part"] == 1:
        print(
            f"Sum of middle elements of the correctly-ordered updates: {get_correct_middle_update_sum(queue)}"
        )
    elif args["part"] == 2:
        print(
            f"Sum of middle elements of the incorrectly-ordered updates: {get_incorrect_middle_update_sum(queue)}"
        )
