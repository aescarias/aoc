import sys

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} [filename]")
    raise SystemExit(1)

filename, *_ = sys.argv[1:]

with open(filename) as fp:
    lines = fp.read().splitlines()


SEARCH_WORDS = (
    "MAS",
    "SAM",
)


def matches_diagonally(lines: list[str], row: int, col: int) -> tuple[bool, bool]:
    space = [line for line in lines[row : row + 3]]
    if len(space) != 3:
        return (False, False)

    top_left_diagonal = (
        space[0][col : col + 1]
        + space[1][col + 1 : col + 2]
        + space[2][col + 2 : col + 3]
    )
    top_right_diagonal = (
        space[0][col + 2 : col + 3]
        + space[1][col + 1 : col + 2]
        + space[2][col : col + 1]
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
        topleft, topright = matches_diagonally(lines, row, col)
        if topleft and topright:
            words += 1

        col += 1

    row += 1

print(words)
