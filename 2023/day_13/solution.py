from __future__ import annotations


def parse(data):
    chunks = data.strip().split("\n\n")
    return [c.split("\n") for c in chunks]


def solve(input):
    return part1(input), part2(input)


def part1(input):
    return sum(ref_finder(c, smudge=0) for c in input)


def part2(input):
    return sum(ref_finder(c, smudge=1) for c in input)


def ref_finder(input, smudge=0):
    for k in range(len(input) - 1):  # horizontal
        if (
            sum(
                1
                for upper, lower in zip(reversed(input[: k + 1]), input[k + 1 :])
                for left, right in zip(upper, lower)
                if left != right
            )
            == smudge
        ):
            return (k + 1) * 100
    for k in range(len(input[0]) - 1):  # vertical
        if (
            sum(
                1
                for row in input
                for left, right in zip(reversed(row[: k + 1]), row[k + 1 :])
                if left != right
            )
            == smudge
        ):
            return k + 1
