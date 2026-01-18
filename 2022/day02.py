"""
Advent of Code 2022 Day 2: Rock Paper Scissors
https://adventofcode.com/2022/day/2
"""

from enum import IntEnum

from aocgen import get_user_input


class Choice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(IntEnum):
    LOSE = 0
    DRAW = 1
    WIN = 2


OPPONENT_MAP: dict[str, Choice] = {
    "A": Choice.ROCK,
    "B": Choice.PAPER,
    "C": Choice.SCISSORS,
}

PLAYER_MAP: dict[str, Choice] = {
    "X": Choice.ROCK,
    "Y": Choice.PAPER,
    "Z": Choice.SCISSORS,
}

OUTCOME_MAP: dict[str, Outcome] = {
    "X": Outcome.LOSE,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

LOSE_SCORE = 0
DRAW_SCORE = 3
WIN_SCORE = 6


def player_score_for_round(opponent: Choice, player: Choice) -> int:
    """Returns the total score for a Rock-Paper-Scissors round (opponent, player)."""

    # total score for player = score of shape chosen + score of game outcome
    match (opponent, player):
        case (
            (Choice.ROCK, Choice.PAPER)
            | (Choice.PAPER, Choice.SCISSORS)
            | (Choice.SCISSORS, Choice.ROCK)
        ):
            return int(player) + WIN_SCORE
        case _ if opponent == player:
            return int(player) + DRAW_SCORE
        case _:
            return int(player) + LOSE_SCORE


def player_move_for_round(opponent: Choice, outcome: Outcome) -> Choice:
    """According to the choice of opponent, returns the move necessary for the
    outcome to occur."""

    match (outcome, opponent):
        case (Outcome.WIN, Choice.ROCK):
            return Choice.PAPER
        case (Outcome.WIN, Choice.PAPER):
            return Choice.SCISSORS
        case (Outcome.WIN, Choice.SCISSORS):
            return Choice.ROCK
        case (Outcome.LOSE, Choice.ROCK):
            return Choice.SCISSORS
        case (Outcome.LOSE, Choice.PAPER):
            return Choice.ROCK
        case (Outcome.LOSE, Choice.SCISSORS):
            return Choice.PAPER
        case (Outcome.DRAW, _):
            return opponent


def part1(lines: list[str]) -> int:
    score_sum = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        opponent_letter, player_letter = line.split()

        opponent_choice = OPPONENT_MAP[opponent_letter]
        player_choice = PLAYER_MAP[player_letter]

        score_sum += player_score_for_round(opponent_choice, player_choice)

    return score_sum


def part2(lines: list[str]) -> int:
    score_sum = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        opponent_letter, outcome_letter = line.split()

        opponent_choice = OPPONENT_MAP[opponent_letter]
        outcome = OUTCOME_MAP[outcome_letter]

        player_choice = player_move_for_round(opponent_choice, outcome)
        score_sum += player_score_for_round(opponent_choice, player_choice)

    return score_sum


if __name__ == "__main__":
    args = get_user_input(2022, 2)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        print(f"The score sum is {part1(lines)}.")
    elif args["part"] == 2:
        print(f"The score sum is {part2(lines)}.")
