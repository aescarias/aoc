import itertools
import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()

page_ordering_rules = []
updates = []

current_section = page_ordering_rules
for line in lines:
    if not line:
        current_section = updates
        continue

    if current_section is page_ordering_rules:
        before, after = list(int(val) for val in line.split("|"))
        current_section.append((before, after))
    else:
        pages = list(int(val) for val in line.split(","))
        current_section.append(pages)


def is_ordered(update: list[int], page_ordering: list[tuple[int, int]]) -> bool:
    for current_page, next_page in itertools.pairwise(update):
        page_order = next(
            item for item in page_ordering if current_page in item and next_page in item
        )
        if (current_page, next_page) != page_order:
            return False

    return True


middle_page_sum = 0

for update in updates:
    if is_ordered(update, page_ordering_rules):
        middle_page_sum += update[len(update) // 2]

print(middle_page_sum)
