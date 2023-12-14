from __future__ import annotations

from itertools import combinations


def parse(data):
    return data.strip().split("\n")


def solve(input):
    return part1(input), part1(input, factor=1_000_000)


def part1(input, factor=2):
    input = expand(input, factor)

    result = 0
    for g1, g2 in combinations(input, 2):
        result += shortest_path(g1, g2)

    return result


def expand(universe, factor=2):
    empty_rows = set()
    empty_cols = set(range(len(universe[0])))

    for i, row in enumerate(universe):
        empty = [j for j, c in enumerate(row) if c == "."]
        if len(empty) == len(row):
            empty_rows.add(i)
        empty_cols.intersection_update(empty)

    result = {}
    di = 0

    for i, row in enumerate(universe):
        dj = 0
        for j, c in enumerate(row):
            if c == "#":
                result[(i + di, j + dj)] = len(result) + 1
            elif j in empty_cols:
                dj += (factor-1)

        if i in empty_rows:
            di += (factor - 1)

    return result


def shortest_path(g1, g2):
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
