from copy import deepcopy


def parse(data):
    state, instructions = data.rstrip().split("\n\n")

    state = state.split("\n")
    stacks = [[] for _ in range(1, len(state.pop()), 4)]

    for line in reversed(state):
        for i, pos in enumerate(range(1, len(line.rstrip()), 4)):
            if c := line[pos].strip():
                stacks[i].append(c)

    instructions = [
        [int(x) for x in line.strip().split()[1::2]]
        for line in instructions.strip().split("\n")
    ]

    return stacks, instructions


def solve(input):
    stacks, instructions = input
    return (
        part1(deepcopy(stacks), instructions),
        part2(stacks, instructions),
    )


def part1(stacks, instructions):
    for num, source, dest in instructions:
        for _ in range(num):
            stacks[dest-1].append(stacks[source-1].pop())

    return "".join(s[-1] for s in stacks)


def part2(stacks, instructions):
    for num, source, dest in instructions:
        payload = []
        for _ in range(num):
            payload.append(stacks[source-1].pop())

        stacks[dest-1].extend(reversed(payload))

    return "".join(s[-1] for s in stacks)
