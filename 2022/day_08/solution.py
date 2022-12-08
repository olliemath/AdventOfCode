def parse(data):
    return [[int(c) for c in line] for line in data.strip().split("\n")]


def solve(input):
    return part1(input), part2(input)


def part1(input):
    visible = 0
    # Could be more efficient, but we don't need it right now
    for i, line in enumerate(input):
        for j, t in enumerate(line):
            if any(
                all(s < t for s in line)
                for line in get_line_of_sight(input, i, j)
            ):
                visible += 1
    return visible


def part2(input):
    scores = []
    for i, line in enumerate(input):
        for j, _ in enumerate(line):
            scores.append(score(input, i, j))

    return max(scores)


def score(input, i, j):
    v = view(input, i, j)
    return v[0] * v[1] * v[2] * v[3]


def get_line_of_sight(input, i, j):
    # lines of sight to the edge of the grid
    return (
        (input[i][k] for k in range(j - 1, -1, -1)),
        (input[i][k] for k in range(j + 1, len(input))),
        (input[k][j] for k in range(i - 1, -1, -1)),
        (input[k][j] for k in range(i + 1, len(input))),
    )


def view(input, i, j):
    t = input[i][j]
    return tuple(
        trees_seen(line, t) for line in get_line_of_sight(input, i, j)
    )


def trees_seen(line, height):
    visibile = 0
    for t in line:
        visibile += 1
        if t >= height:
            break

    return visibile
