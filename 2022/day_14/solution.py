import math


def parse(data):
    rock = set()
    for line in data.strip().split("\n"):
        pairs = [
            tuple(map(int, p.strip().split(",")))
            for p in line.strip().split("->")
        ]
        for (sx, sy), (ex, ey) in zip(pairs, pairs[1:]):
            if sx != ex:
                start = min(sx, ex)
                end = max(sx, ex)
                for x in range(start, end + 1):
                    rock.add((x, sy))
            elif sy != ey:
                start = min(sy, ey)
                end = max(sy, ey)
                for y in range(start, end + 1):
                    rock.add((sx, y))
            else:
                rock.add((sx, sy))

    return rock


def solve(input):
    return part1(input), part2(input)


def part1(input):
    ybound = max(y for _, y in input)
    ocupado = set(input)

    while True:
        pos, final = (500, 0), False

        while not final:
            pos, final = step(pos, ocupado)
            if pos[1] > ybound:
                return len(ocupado) - len(input)

        ocupado.add(pos)


def part2(input):
    ybound = max(y for _, y in input)
    ocupado = set(input)

    while True:
        pos, final = (500, 0), False

        while not final:
            pos, final = step(pos, ocupado, ybound + 2)

        ocupado.add(pos)
        if (500, 0) in ocupado:
            return len(ocupado) - len(input)


def step(pos, ocupado, ymax=math.inf):
    x, y = pos
    for candidate in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1)):
        if candidate not in ocupado and y + 1 < ymax:
            return candidate, False

    return pos, True
