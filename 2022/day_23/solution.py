from collections import defaultdict, deque


def parse(data):
    # return [list(line) for line in data.strip().split("\n")]
    grid = set()
    for y, line in enumerate(data.strip().split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                grid.add((x, y))
    return grid


def solve(input):
    return part1(input), part2(input)


def part1(input):
    grid = input.copy()
    checks = new_checks()

    for _ in range(10):
        step(grid, checks)

    minx, maxx = min(p[0] for p in grid), max(p[0] for p in grid)
    miny, maxy = min(p[1] for p in grid), max(p[1] for p in grid)
    return (1 + maxx - minx) * (1 + maxy - miny) - len(grid)


def part2(input):
    grid = input.copy()
    checks = new_checks()

    try:
        for k in range(1, 10_000):
            step(grid, checks)
    except StopIteration:
        return k


def step(grid, checks):
    to_move = defaultdict(list)  # to: from
    for (x, y) in grid:
        neighbours = collect_neighbours(x, y, grid)
        if not neighbours:
            continue
        for move, scans in checks:
            for dx, dy in scans:
                if (x + dx, y + dy) in neighbours:
                    break
            else:
                to_move[(x + move[0], y + move[1])].append((x, y))
                break

    if not to_move:
        raise StopIteration

    for to_, from_ in to_move.items():
        if len(from_) == 1:
            grid.add(to_)
            grid.remove(from_[0])

    checks.rotate(-1)


def new_checks():
    return deque([
        ((0, -1), ((-1, -1), (0, -1), (1, -1))),  # N
        ((0, 1), ((-1, 1), (0, 1), (1, 1))),  # S
        ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),  # W
        ((1, 0), ((1, -1), (1, 0), (1, 1))),  # E
    ])


def collect_neighbours(x, y, grid):
    result = set()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            xn, yn = x + dx, y + dy
            if (xn, yn) != (x, y) and (xn, yn) in grid:
                result.add((xn, yn))
    return result
