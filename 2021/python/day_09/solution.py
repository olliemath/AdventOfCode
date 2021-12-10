def parse(input):
    lines = [line.strip() for line in input.strip().split("\n")]
    return lines


def solve(input):
    return compute1(input), compute2(input)


def find_lowpoints(input):
    lowpoints = []
    for i, line in enumerate(input):
        for j, char in enumerate(line):
            if (
                (i == 0 or input[i-1][j] > char)
                and (j == 0 or line[j-1] > char)
                and (i == len(input) - 1 or input[i+1][j] > char)
                and (j == len(line) - 1 or line[j + 1] > char)
            ):
                lowpoints.append((i, j, char))

    return lowpoints


def compute1(input):
    lowpoints = find_lowpoints(input)

    return sum(map(lambda l: int(l[2]), lowpoints)) + len(lowpoints)


def compute2(input):
    basins = sorted(get_basins(input))
    return basins[-3] * basins[-2] * basins[-1]


def get_basins(input):
    basins = []
    for i, j, c in find_lowpoints(input):
        basins.append(len(get_basin(input, i, j, c)))
    return basins


def get_basin(input, i, j, c, seen=None):
    if seen is None:
        seen = {(i, j)}
    else:
        seen.add((i, j))

    if i > 0 and input[i-1][j] > c and input[i-1][j] != "9":
        if (i-1, j) not in seen:
            get_basin(input, i-1, j, input[i-1][j], seen)
    if j > 0 and input[i][j-1] > c and input[i][j-1] != "9":
        if (i, j-1) not in seen:
            get_basin(input, i, j-1, input[i][j-1], seen)
    if i < len(input) - 1 and input[i+1][j] > c and input[i+1][j] != "9":
        if (i+1, j) not in seen:
            get_basin(input, i+1, j, input[i+1][j], seen)
    if j < len(input[0]) - 1 and input[i][j+1] > c and input[i][j+1] != "9":
        if (i, j+1) not in seen:
            get_basin(input, i, j+1, input[i][j+1], seen)

    return seen
