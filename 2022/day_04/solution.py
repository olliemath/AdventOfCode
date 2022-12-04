def parse(data):
    parsed = []
    for pair in data.strip().split("\n"):
        elf1, elf2 = pair.split(",")
        elf1 = tuple(map(int, elf1.split("-")))
        elf2 = tuple(map(int, elf2.split("-")))
        parsed.append((elf1, elf2))
    return parsed


def solve(input):
    part1 = sum(1 for pair in input if subset(*pair))
    part2 = sum(1 for pair in input if overlap(*pair))
    return part1, part2


def subset(e1, e2):
    return (
        (e1[0] <= e2[0] and e1[1] >= e2[1])
        or (e1[0] >= e2[0] and e1[1] <= e2[1])
    )


def overlap(e1, e2):
    return (
        e1[0] <= e2[0] <= e1[1]
        or e1[0] <= e2[1] <= e1[1]
        or e2[0] <= e1[0] <= e2[1]
        or e2[0] <= e1[1] <= e2[1]
    )
