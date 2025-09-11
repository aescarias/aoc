# Tekgar's Advent of Code

**Solutions** for [Advent of Code](https://adventofcode.com) written in Python.

## About the solutions

In this repository, you will find folders representing a year of Advent of Code. Inside of each folder you will find the solutions as individual Python files in the format of `dayN.py` where `N` represents a solution for a particular day (1 through 25).

Each solution file can be run independently and includes documentation & notes on the particular puzzle. These solutions currently assume you're using Python 3.11 or later and can be run like this:

```sh
# (from the project root)
python -m 2024.day1 1 -I your_input_file.txt
```

Each solution takes an argument `part` and optionally a flag `-I/--input`. The `part` argument specifies the part of the solution to run (if you aren't familiar with Advent of Code, each puzzle is split into two parts -- the second usually being a twist on the first).

The `-I/--input` flag specifies the input file that will be used to run the solution. Input files cannot be released publicly so you must obtain your own by logging into Advent of Code and downloading it (see [Retrieving your session token](./aocgen/README.md#retrieving-your-session-token) in the `aocgen` README for details).

In the case the `-I` flag is not provided, the solution will look for an input file in an `inputs` folder. The `inputs` folder is divided into folders representing each year. Each folder may include input files with names in the form of `dayN_input.txt` where `N` represents the day the input is for.

## About aocgen

aocgen is a utility for generating boilerplate for Advent of Code solutions. More information about aocgen can be found in its [README](./aocgen/README.md) file.

## About aocutils

aocutils includes personal utilities for making Advent of Code less repetitive. More information about aocutils can be found in its [README](./aocutils/README.md) file.
