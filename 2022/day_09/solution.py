def parse(data):
    for line in data.strip().split("\n"):
        d, x = line.strip().split()
        if d == "L":
            yield (-int(x), 0)
        elif d == "R":
            yield (int(x), 0)
        elif d == "U":
            yield (0, int(x))
        else:
            yield (0, -int(x))


def solve(input):
    input = list(input)
    return simulate(input, 2), simulate(input, 10)


def simulate(input, length):
    visited = {(0, 0)}
    rope = [[0, 0] for _ in range(length)]

    for dx, dy in input:
        if dx:
            n, d, ix = abs(dx), int(dx / abs(dx)), 0
        elif dy:
            n, d, ix = abs(dy), int(dy / abs(dy)), 1

        for _ in range(n):
            rope[0][ix] += d  # head

            for hpos, tpos in zip(rope, rope[1:]):
                if linf(hpos, tpos) > 1:
                    if hpos[0] < tpos[0]:
                        tpos[0] -= 1
                    elif hpos[0] > tpos[0]:
                        tpos[0] += 1
                    if hpos[1] < tpos[1]:
                        tpos[1] -= 1
                    elif hpos[1] > tpos[1]:
                        tpos[1] += 1

            visited.add(tuple(rope[-1]))

    return len(visited)


def linf(v, w):
    return max(abs(a - b) for a, b in zip(v, w))


def print_grid(h, t):
    print()
    for i in range(4, -1, -1):
        row = ""
        for j in range(0, 6):
            if [j, i] == h:
                row += "H"
            elif [j, i] == t:
                row += "T"
            else:
                row += "."
        print(row)


def print_final(ts):
    print()
    for i in range(4, -1, -1):
        row = ""
        for j in range(0, 6):
            if (j, i) in ts:
                row += "#"
            else:
                row += "."
        print(row)
