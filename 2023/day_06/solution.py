from __future__ import annotations

import math


def parse(data):
    chunks = data.strip().split("\n")
    chunks = [list(map(int, c.split(":")[1].split())) for c in chunks]
    parsed = tuple(zip(chunks[0], chunks[1], strict=True))
    return parsed


def solve(input):
    return part1(input), part2(input)


def part1(input):
    result = 1
    for time, record in input:
        min_, max_ = solve_quadratic(time, record)
        result *= 1 + max_ - min_
    return result


def part2(input):
    # Need to re-parse :/
    times, records = zip(*input)
    time = int("".join(map(str, times)))
    record = int("".join(map(str, records)))

    min_, max_ = solve_quadratic(time, record)
    return 1 + max_ - min_


def solve_quadratic(time, record):
    # Need find x such that x**2 - time * x + record = -1
    # Use the quadratic formula:
    #  (-b +- sqrt(b**2 - 4ac)) / 2
    determinant = math.sqrt(time**2 - 4 * (record + 1))
    return math.ceil((time - determinant) / 2), math.floor((time + determinant) / 2)
