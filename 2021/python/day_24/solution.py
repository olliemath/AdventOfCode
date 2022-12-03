def num_if_num(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse(input):
    return [
        [num_if_num(x) for x in line.split()]
        for line in input.strip().split("\n")
    ]


def solve(input):
    solutions = backsolve(INS, 0, [])
    inputs = [tuple(reversed(s)) for s in solutions]
    numbers = ["".join(map(str, input)) for input in inputs]
    print(len(numbers))
    return max(numbers), min(numbers)


def step(i, a, b, c, z):
    x = (z % 26 + b) != i
    return (z // a) * (25 * x + 1) + (i + c) * x


def backstep(a, b, c, z1):
    # Two cases x = 1 or x = 0
    for i in range(9, 0, -1):
        # x = 0 => z1 = z0//a
        for a0 in range(a):
            z0 = a0 + a * z1
            if step(i, a, b, c, z0) == z1:
                yield i, z0

    # x = 1:
    for i in range(9, 0, -1):
        for a0 in range(a):
            z0 = a0 + a * (z1 - i - c) // 26
            if step(i, a, b, c, z0) == z1:
                yield i, z0


def backsolve(steps, z, path):
    step = steps.pop()

    a, b, c = step
    prev = {}
    for i, pz in backstep(a, b, c, z):
        if pz not in prev or i > prev[pz]:
            prev[pz] = i

    if not prev:
        steps.append(step)
        return []

    paths = []
    for z_new, i in prev.items():
        if not steps:
            paths.append(path + [i])
        else:
            path.append(i)
            paths.extend(backsolve(steps, z_new, path))
            path.pop()

    steps.append(step)
    return paths


INS = [
    (1, 12, 6),
    (1, 10, 6),
    (1, 13, 3),
    (26, -11, 11),
    (1, 13, 9),
    (26, -1, 3),
    (1, 10, 13),
    (1, 11, 6),
    (26, 0, 14),
    (1, 10, 10),
    (26, -5, 12),
    (26, -16, 10),
    (26, -7, 11),
    (26, -11, 15),
]
