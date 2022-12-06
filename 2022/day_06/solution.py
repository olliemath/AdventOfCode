def parse(data):
    return data.strip()


def solve(input):
    return part1(input), part2(input)


def part1(input):
    for k in range(len(input)):
        chars = input[k:k+4]
        if len(set(chars)) == 4:
            return k + 4


def part2(input):
    for k in range(len(input)):
        chars = input[k:k+14]
        if len(set(chars)) == 14:
            return k + 14
