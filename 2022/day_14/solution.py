def parse(data):
    rocks = set()
    horizontals = []
    for line in data.strip().split("\n"):
        pairs = [
            tuple(map(int, p.strip().split(",")))
            for p in line.strip().split("->")
        ]
        for (sx, sy), (ex, ey) in zip(pairs, pairs[1:]):
            if sx != ex:
                start = min(sx, ex)
                end = max(sx, ex)
                segment = []
                for x in range(start, end + 1):
                    rock = (x, sy)
                    segment.append(rock)
                    rocks.add(rock)
                horizontals.append(segment)

            elif sy != ey:
                start = min(sy, ey)
                end = max(sy, ey)
                for y in range(start, end + 1):
                    rocks.add((sx, y))

    return rocks, horizontals


def solve(input):
    maxy = max(y for _, y in input[0]) + 2
    minx = min(x for x, _ in input[0]) - maxy
    maxx = max(x for x, _ in input[0]) + maxy

    grid1 = [["." for _ in range(minx, maxx + 1)] for _ in range(maxy + 1)]
    for x, y in input[0]:
        grid1[y][x - minx] = "#"

    grid2 = [row[:] for row in grid1]
    grid2[-1] = ["#" for _ in range(len(grid2[-1]))]

    sourcex = 500 - minx
    sourcey = 0

    return (
        part1(grid1, sourcex, sourcey),
        part2(grid2, sourcex, sourcey),
    )


def part1(grid, sourcex, sourcey):
    sand = 0
    while True:
        try:
            drop_sand(grid, sourcex, sourcey)
            sand += 1
        except IndexError:
            return sand


def part2(grid, sourcex, sourcey):
    sand = 0
    while grid[sourcey][sourcex] != "o":
        drop_sand(grid, sourcex, sourcey)
        sand += 1
        # printgrid(grid)

    return sand


def drop_sand(grid, sourcex, sourcey):
    x, y = sourcex, sourcey
    while True:
        if grid[y + 1][x] == ".":
            y += 1
        elif grid[y + 1][x - 1] == ".":
            y += 1
            x -= 1
        elif grid[y + 1][x + 1] == ".":
            y += 1
            x += 1
        else:
            grid[y][x] = "o"
            return


def printgrid(grid):
    print()
    for row in grid:
        print("".join(row))
