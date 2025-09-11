# aocgen

`aocgen` is a utility that allows you to quickly generate a solution template and retrieve the inputs for a particular day of Advent of Code. It is designed to reduce the boilerplate common in a lot of these puzzles.

## Usage

You may run this utility as seen in the example below:

```sh
# (from the project root)
python -m aocgen 2024 9 -T "Disk Fragmenter"
```

aocgen takes 2 arguments and 2 flags. The first argument is for a year in Advent of Code. The second argument is for a particular day in such year.

The 2 flags available are `-T/--title` and `-K/--key` (both optional).

- The first flag specifies the puzzle's title which is included in the output file as documentation. If no title is specified, the value included will be `[untitled]`.
- The second flag specifies the file including your Advent of Code session token. If not specified, one of two alternative methods may be used to provide it, as described below.

### Retrieving your session token

Each Advent of Code user is assigned a customized set of inputs. Inputs cannot be shared publicly so you must obtain your own via the website.

For ``aocgen`` to retrieve these inputs, it requires a **session token.**

To get your session token:

1. Log in to Advent of Code and open Developer Tools.
2. Go to the Storage tab in Firefox or the Application tab in Chrome.
3. Open the Cookies tab and copy the value in the `session` key.

After completing these steps, you may provide your session token using one of three methods (listed in order of most precedence):

- Setting the `AOC_SESSION_TOKEN` environment variable.
- Providing the name of the file storing the key via the `-K/--key` flag.
- Creating a `TOKEN` file with the key as its content in the directory you're running aocgen from.

If you don't provide a session token (or `aocgen` was unable to find one), you will be asked to provide it via the command line.

If you do not wish to provide a session token, you may dismiss this prompt if asked, or alternatively, set the session token to `never` using one of the three methods above so aocgen knows not to ask for a token next time. With no session token, however, aocgen will be unable to retrieve your puzzle inputs.
