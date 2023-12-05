def parse(data):
    lines = data.strip().split("\n")
    lines = [line.strip().split(": ")[1] for line in lines]
    lines = [line.split(" | ") for line in lines]
    return [(list(map(int, lh.split())), list(map(int, rh.split()))) for lh, rh in lines]


def solve(input):
    return sum(part1(input)), part2(input)


def part1(input):
    scores = []
    for lh, rh in input:
        lh = set(lh)
        scores.append(int(2 ** (sum(1 for n in rh if n in lh) - 1)))

    return scores


def part2(input):
    counts = {n: 1 for n in range(len(input))}

    for n, (lh, rh) in enumerate(input):
        lh = set(lh)
        won = sum(1 for n in rh if n in lh)
        for i in range(1, won + 1):
            counts[n + i] += counts[n]

    return sum(counts.values())
