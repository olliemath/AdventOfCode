from __future__ import annotations


def parse(data):
    return data.strip().split("\n")


def solve(input):
    return part1(input), part2(input)


def part1(input, start=(0, -1), dir=">"):
    path = trace(input, start, dir)
    return len(set(v for v, _ in path))


def part2(input):
    largest = 0
    for x in range(len(input)):
        largest = max(largest, part1(input, (x, -1), ">"))
        largest = max(largest, part1(input, (x, len(input[0])), "<"))

    for y in range(len(input[0])):
        largest = max(largest, part1(input, (-1, y), "v"))
        largest = max(largest, part1(input, (len(input), y), "^"))

    return largest


DIRECTION_MAPS = {
    "/": {">": ["^"], "v": ["<"], "^": [">"], "<": ["v"]},
    "\\": {">": ["v"], "^": ["<"], "v": [">"], "<": ["^"]},
    "-": {">": [">"], "<": ["<"], "^": [">", "<"], "v": [">", "<"]},
    "|": {"^": ["^"], "v": ["v"], ">": ["v", "^"], "<": ["v", "^"]},
    ".": {">": [">"], "^": ["^"], "<": ["<"], "v": ["v"]},
}
TRANSITIONS = {
    ">": lambda v: (v[0], v[1] + 1),
    "<": lambda v: (v[0], v[1] - 1),
    "v": lambda v: (v[0] + 1, v[1]),
    "^": lambda v: (v[0] - 1, v[1]),
}


def trace(input, start, dir):
    seen = set()
    queue = [(start, dir)]
    while queue:
        vertex, dir = queue.pop()
        new = TRANSITIONS[dir](vertex)
        if not (0 <= new[0] < len(input) and 0 <= new[1] < len(input[0])):
            continue

        char = input[new[0]][new[1]]
        for newdir in DIRECTION_MAPS[char][dir]:
            if (new, newdir) not in seen:
                seen.add((new, newdir))
                queue.append((new, newdir))

    return seen
