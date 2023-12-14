from __future__ import annotations


def parse(data):
    return [list(line) for line in data.strip().split("\n")]


def solve(input):
    return part1(input), part2(input)


def part1(input):
    grid = north(input)
    return sum(len(grid) - n for n, row in enumerate(grid) for c in row if c == "O")


def part2(grid, cycles=1_000_000_000):
    seen = [grid]

    k = 0
    while k < cycles:
        grid = cycle(grid)
        k += 1

        for i, old in enumerate(seen):
            if grid == old:
                # skip to the end
                grid = seen[i + (cycles - k) % (k - i)]
                k = cycles
                break

        seen.append(grid)

    return sum(len(grid) - n for n, row in enumerate(grid) for c in row if c == "O")


def cycle(grid):
    grid = north(grid)
    grid = west(grid)
    grid = south(grid)
    grid = east(grid)
    return grid


def north(grid):
    columns = [[] for _ in range(len(grid[0]))]
    for k in range(len(grid[0])):
        for j, row in enumerate(grid):
            if row[k] == "O":
                columns[k].append("O")
            elif row[k] == "#":
                while len(columns[k]) < j:
                    columns[k].append(".")
                columns[k].append("#")

        columns[k].extend("." for _ in range(len(grid) - len(columns[k])))

    return [list(t) for t in zip(*columns)]


def south(grid):
    columns = [[] for _ in range(len(grid[0]))]
    for k in range(len(grid[0])):
        for j, row in enumerate(reversed(grid)):
            if row[k] == "O":
                columns[k].append("O")
            elif row[k] == "#":
                while len(columns[k]) < j:
                    columns[k].append(".")
                columns[k].append("#")

        columns[k].extend("." for _ in range(len(grid) - len(columns[k])))

    return [list(t) for t in zip(*(reversed(c) for c in columns))]


def west(grid):
    rows = []
    for row in grid:
        newrow = []
        for i, char in enumerate(row):
            if char == "O":
                newrow.append("O")
            elif char == "#":
                while len(newrow) < i:
                    newrow.append(".")
                newrow.append("#")

        newrow.extend("." for _ in range(len(grid[0]) - len(newrow)))
        rows.append(newrow)

    return rows


def east(grid):
    rows = []
    for row in grid:
        newrow = []
        for i, char in enumerate(reversed(row)):
            if char == "O":
                newrow.append("O")
            elif char == "#":
                while len(newrow) < i:
                    newrow.append(".")
                newrow.append("#")

        newrow.extend("." for _ in range(len(grid[0]) - len(newrow)))
        rows.append(list(reversed(newrow)))

    return rows
