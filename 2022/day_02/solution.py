outcomes = {
    "A": {"X": 3, "Y": 6, "Z": 0},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 6, "Y": 0, "Z": 3},
}
shape_scores = {a: i + 1 for i, a in enumerate("XYZ")}

shape_scores_2 = {
    "A": {"X": 3, "Y": 1, "Z": 2},
    "B": {"X": 1, "Y": 2, "Z": 3},
    "C": {"X": 2, "Y": 3, "Z": 1},
}
outcomes_2 = {a: i * 3 for i, a in enumerate("XYZ")}


def parse(data):
    for game in data.strip().split("\n"):
        yield game.split()


def solve(input):
    input = list(input)
    return part1(input), part2(input)


def part1(input):
    return sum(shape_scores[us] + outcomes[them][us] for them, us in input)


def part2(input):
    return sum(
        outcomes_2[out] + shape_scores_2[them][out] for them, out in input
    )
