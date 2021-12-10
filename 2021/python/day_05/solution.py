from collections import defaultdict


def parse(input):
    pairs = []
    for line in input.split("\n"):
        if not line.strip():
            continue

        pair1, pair2 = line.strip().split(" -> ")
        pair1 = tuple(map(int, pair1.split(",")))
        pair2 = tuple(map(int, pair2.split(",")))
        pairs.append((pair1, pair2))

    return pairs


def solve(input):
    grid_1 = compute(input, False)
    grid_2 = compute(input, True)

    sol1 = sum(1 for r in grid_1.values() for c in r.values() if c > 1)
    sol2 = sum(1 for r in grid_2.values() for c in r.values() if c > 1)

    return sol1, sol2


def compute(pairs, diagonals=False):

    # Throw out diagonals?
    if not diagonals:
        pairs = [
            p for p in pairs if p[0][0] == p[1][0] or p[0][1] == p[1][1]
        ]

    # Build grid
    grid = defaultdict(lambda: defaultdict(int))

    for p1, p2 in pairs:
        x1, y1 = p1
        x2, y2 = p2
        if y1 == y2:
            row = grid[y1]
            for x in range(min(x1, x2), max(x1, x2)+1):
                row[x] += 1
        elif x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                grid[y][x1] += 1
        else:
            # This is directional
            xdir = 1 if x1 <= x2 else -1
            ydir = 1 if y1 <= y2 else -1
            for x, y in zip(
                range(x1, x2+xdir, xdir), range(y1, y2+ydir, ydir)
            ):
                grid[y][x] += 1

    return grid
