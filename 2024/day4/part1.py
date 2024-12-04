import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()


SEARCH_WORDS = ("XMAS", "SAMX")


def matches_horizontally(lines: list[str], row: int, col: int) -> bool:
    return row < len(lines) and lines[row][col:].startswith(SEARCH_WORDS)


def matches_vertically(lines: list[str], row: int, col: int) -> bool:
    return "".join(line[col : col + 1] for line in lines[row : row + 4]).startswith(
        SEARCH_WORDS
    )


def matches_diagonally(lines: list[str], row: int, col: int) -> tuple[bool, bool]:
    space = [line for line in lines[row : row + 4]]
    if len(space) != 4:
        return (False, False)

    top_left_diagonal = (
        space[0][col : col + 1]
        + space[1][col + 1 : col + 2]
        + space[2][col + 2 : col + 3]
        + space[3][col + 3 : col + 4]
    )
    top_right_diagonal = (
        space[0][col + 3 : col + 4]
        + space[1][col + 2 : col + 3]
        + space[2][col + 1 : col + 2]
        + space[3][col : col + 1]
    )

    return (
        top_left_diagonal.startswith(SEARCH_WORDS),
        top_right_diagonal.startswith(SEARCH_WORDS),
    )


words = 0
row = 0

while row < len(lines):
    line = lines[row]

    col = 0
    while col < len(line):
        words += sum(
            (
                matches_horizontally(lines, row, col),
                matches_vertically(lines, row, col),
                *matches_diagonally(lines, row, col),
            )
        )

        col += 1

    row += 1

print(words)
