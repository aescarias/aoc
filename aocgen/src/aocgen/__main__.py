import argparse
import getpass
import pathlib
import string

from . import InputFetchError, get_puzzle_input, load_session_token


class Style:
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    LINED = "\x1b[4m"

    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"


AOC_TEMPLATE = """\"\"\"
Advent of Code $year Day $day: $title
https://adventofcode.com/$year/day/$day
\"\"\"

from aocgen import get_user_input

# solution here

if __name__ == "__main__":
    args = get_user_input($year, $day)

    with args["input_file"] as fp:
        lines = fp.read().splitlines()

    if args["part"] == 1:
        ...  # first part solution
    elif args["part"] == 2:
        ...  # second part solution
"""


SESSION_TOKEN_MESSAGE = f"""{Style.RED}No session token provided.{Style.RESET}

Advent of Code assigns different inputs to each user. To retrieve your custom inputs, 
you must provide your {Style.BOLD}session token{Style.RESET}.

To retrieve your session token, you must log in to Advent of Code, open DevTools, then 
go to the Storage tab in Firefox (or Application tab in Chrome), then Cookies, and copy 
the value of the 'session' key into the prompt below.

The input provided will be stored in a {Style.BOLD}TOKEN{Style.RESET} file which will be 
used by aocgen for future runs. You may also set the {Style.BOLD}AOC_SESSION_TOKEN{Style.RESET} 
environment variable to load the token automatically.

As the name suggests, keep your token private. {Style.BOLD}{Style.LINED}{Style.RED}DO NOT SHARE{Style.RESET}.
"""


def write_solution(year: int, day: int, title: str) -> bool:
    template = string.Template(AOC_TEMPLATE)
    output = template.substitute(year=year, day=day, title=title)

    output_path = pathlib.Path(str(year)) / f"day{day}.py"
    output_path.parent.mkdir(exist_ok=True)

    if output_path.exists():
        return False

    output_path.write_text(output)
    return True


def confirm(prompt: str) -> bool:
    result = ""
    while result not in ("y", "n"):
        result = input(prompt).lower()

    return result == "y"


def write_input(year: int, day: int, key: str) -> tuple[bool, str]:
    puzzle_input_path = pathlib.Path("inputs") / str(year) / f"day{day}_input.txt"
    puzzle_input_path.parent.mkdir(parents=True, exist_ok=True)

    if puzzle_input_path.exists():
        overwrite = confirm(
            f"{Style.YELLOW}W:{Style.RESET} Input file for day {day} already exists. "
            "Confirm overwrite (y/n)? "
        )
    else:
        overwrite = True

    if not overwrite:
        return (False, "EXISTS")

    if key and (p := pathlib.Path(key)).exists():
        key_path = p
    else:
        print(
            f"{Style.YELLOW}W:{Style.RESET} -K/--key was not provided or does not exist. Looking for "
            "TOKEN file or AOC_SESSION_TOKEN variable."
        )
        key_path = None

    token = load_session_token(key_path)
    if token is None:
        print(SESSION_TOKEN_MESSAGE)
        token = getpass.getpass("Session token [leave empty to dismiss]: ").strip()

        if not token:
            return (False, "DENIED")

        pathlib.Path("TOKEN").write_text(token)

    try:
        text = get_puzzle_input(year, day, token)
        puzzle_input_path.write_text(text)
        return (True, "")
    except InputFetchError as exc:
        print(f"{Style.RED}E:{Style.RESET} {exc}")
        print(f"{Style.RED}E:{Style.RESET} No input will be added.")
        return (False, "ERROR")


def run_setup_cli() -> None:
    parser = argparse.ArgumentParser(
        prog="aocgen", description="Create a template for your Advent of Code solution."
    )

    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("-T", "--title", type=str, required=False, default="[untitled]")
    parser.add_argument("-K", "--key", type=str, required=False, default="TOKEN")

    args = parser.parse_args()

    solution_written = write_solution(args.year, args.day, args.title)
    if solution_written:
        print(f"{Style.GREEN}Solution file was written successfully.{Style.RESET}")
    else:
        print(
            f"{Style.YELLOW}W:{Style.RESET} Solution file for day {args.day} already exists. "
            "Will not overwrite."
        )

    input_written, reason = write_input(args.year, args.day, args.key)
    if input_written:
        print(f"{Style.GREEN}Input file was written successfully.{Style.RESET}")
    elif reason == "DENIED":
        print(f"{Style.RED}E:{Style.RESET} User decStyle.lined request.")
    elif reason == "EXISTS":
        print(
            f"{Style.RED}E:{Style.RESET} Input file for day {args.day} already exists. "
            "Will not overwrite."
        )


if __name__ == "__main__":
    run_setup_cli()
