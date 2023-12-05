def parse(data):
    games = []
    for line in data.strip().split("\n"):
        game = []
        for round_ in line.split(":")[1].strip().split("; "):
            game.append({sample.split()[1]: int(sample.split()[0]) for sample in round_.split(", ")})

        games.append(game)

    return games


def solve(input):
    return part1(input), part2(input)


def part1(input):
    total = 0

    for n, game in enumerate(input):
        for round_ in game:
            if round_.get("red", 0) > 12 or round_.get("green", 0) > 13 or round_.get("blue", 0) > 14:
                break
        else:
            total += n + 1

    return total


def part2(input):
    total = 0

    for game in input:
        r, g, b = 0, 0, 0

        for round_ in game:
            r = max(r, round_.get("red", 0))
            g = max(g, round_.get("green", 0))
            b = max(b, round_.get("blue", 0))

        power = r * g * b
        total += power

    return total
