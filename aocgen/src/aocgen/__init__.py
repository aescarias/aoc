import argparse
import os
from io import TextIOWrapper
from pathlib import Path
from typing import TypedDict

import requests

__version__ = "0.1.0"


class Arguments(TypedDict):
    input_file: TextIOWrapper
    part: int


class InputFetchError(Exception):
    pass


def load_session_token(fallback: Path | None = None) -> str | None:
    session_token = os.environ.get("AOC_SESSION_TOKEN")
    if session_token:
        return session_token

    fallback = fallback or Path("TOKEN")
    if fallback.exists():
        return fallback.read_text()


def get_puzzle_input(year: int, day: int, session_token: str) -> str:
    aoc_rs = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": session_token},
        headers={"User-Agent": "aescarias/aocgen (contact=lotta.dev@outlook.com)"},
    )
    if not aoc_rs.ok:
        raise InputFetchError(
            f"Could not fetch input due to {aoc_rs.status_code} {aoc_rs.reason}: {aoc_rs.text!r}"
        )

    return aoc_rs.text


def get_user_input(year: int, day: int) -> Arguments:
    """Gets the command line arguments for the puzzle input."""

    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument(
        "--input",
        "-I",
        type=argparse.FileType("r"),
        default=f"inputs/{year}/day{day}_input.txt",
    )

    args = parser.parse_args()

    return {"input_file": args.input, "part": args.part}
