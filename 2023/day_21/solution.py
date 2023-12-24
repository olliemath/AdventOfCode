from __future__ import annotations


def parse(data):
    return data.strip().split("\n")


def solve(input):
    return part1(input, 64), part2(input, 26501365)


def runner(input, odd=False, max_rounds=1000):
    # figure out the start
    start = get_start(input)
    would_end_on = set()
    front = {start}

    for k in range(1, max_rounds + 1):
        new_front = set()
        for i, j in front:
            for new in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if new in would_end_on:
                    continue
                elif input[new[0] % len(input)][new[1] % len(input[0])] == "#":
                    continue
                else:
                    new_front.add(new)
                    if k % 2 == int(odd):
                        # we will find our way back here
                        would_end_on.add(new)

            front = new_front

        front = new_front
        yield len(would_end_on)


def part1(input, rounds):
    return nth(runner(input), rounds)


def part2(input, rounds):
    offset = rounds % (2 * len(input))
    multip = rounds // (2 * len(input))

    if multip < 1:
        return part1(input, rounds)

    runs = []
    deltas = []
    double_deltas = []

    iterator = runner(input, odd=bool(rounds % 2), max_rounds=1000)
    runs.append(nth(iterator, offset))

    for _ in range(9):
        runs.append(nth(iterator, 2 * len(input)))
        if len(runs) > 1:
            deltas.append(runs[-1] - runs[-2])
        if len(deltas) > 1:
            double_deltas.append(deltas[-1] - deltas[-2])

        if len(double_deltas) > 1 and double_deltas[-1] == double_deltas[-2]:
            break

    if multip < len(runs):
        return runs[multip]

    total = runs[-1]
    delta = deltas[-1]
    double_delta = double_deltas[-1]

    left = multip + 1 - len(runs)
    total += left * (delta + double_delta) + (left * (left - 1) * double_delta) // 2

    return total


def get_start(input):
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if char == "S":
                return (i, j)


def nth(iterator, n):
    for _ in range(n - 1):
        next(iterator)
    return next(iterator)
