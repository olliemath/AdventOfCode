from collections import deque


SHAPES = [
    ["@@@@"],
    [".@.", "@@@", ".@."],
    ["..@", "..@", "@@@"],
    ["@", "@", "@", "@"],
    ["@@", "@@"],
]


def parse(data):
    return data.strip()


def solve(input):
    return max(part1(input)), max(part1(input, 1_000_000_000_000))


def part1(jets, N=2022):
    jets = deque(jets)
    shapes = deque(SHAPES)
    spotter = DuplicateSpotter()

    grid = [["~" for _ in range(7)]]
    k = 0
    offset = 0
    while k < N:
        rock = shapes[0]
        last_seen = spotter(k, grid, jets, rock)
        if last_seen is not None:
            print(last_seen)
            rocks_added = k - last_seen[0]
            height_added = len(grid) - last_seen[1]

            num_cycles = (N - k) // rocks_added
            k += num_cycles * rocks_added
            offset += num_cycles * height_added

        shapes.rotate(-1)
        grid = drop_rock(rock, jets, grid)
        k += 1

    return maxify(grid, offset)


def part2(jets):
    pass


def drop_rock(rock, jets, grid):
    grid = [
        [".", "."] + list(row) + ["." for _ in range(7 - len(row) - 2)]
        for row in rock
    ] + [["." for _ in range(7)] for _ in range(3)] + grid

    at_rest = False
    while True:
        jet = jets[0]
        jets.rotate(-1)
        if jet == "<":
            blocked = False
            for row in grid:
                prev = "#"
                for char in row:
                    if char == "@" and prev == "#":
                        blocked = True
                        break
                    prev = char
                if blocked:
                    break
            if not blocked:
                for row in grid:
                    for i, char in enumerate(row):
                        if char == "@":
                            row[i - 1], row[i] = char, "."

        elif jet == ">":
            blocked = False
            for row in grid:
                nxt = "#"
                for char in reversed(row):
                    if char == "@" and nxt == "#":
                        blocked = True
                        break
                    nxt = char
                if blocked:
                    break
            if not blocked:
                for row in grid:
                    for i in range(len(row) - 1, 0, -1):
                        if row[i - 1] == "@":
                            row[i - 1], row[i] = ".", "@"

        # Check we don't hit anything
        for i, row in enumerate(grid):
            if i == len(grid) - 1:
                break
            for j, char in enumerate(row):
                if char == "@":
                    if grid[i + 1][j] in ("#", "~"):
                        at_rest = True
                        break

        if at_rest:
            for row in grid:
                for j, char in enumerate(row):
                    if char == "@":
                        row[j] = "#"

        else:
            # Drop @s by 1 row
            for i in range(len(grid) - 1, 0, -1):
                prevrow = grid[i - 1]
                for j, char in enumerate(prevrow):
                    if char == "@":
                        prevrow[j], grid[i][j] = ".", "@"

        if at_rest:
            break

    # prune the new grid
    blank = 0
    for row in grid:
        if "#" not in row:
            blank += 1
        else:
            break

    return grid[blank:]


def printgrid(grid):
    return
    print()
    for row in grid:
        print("".join(row))
    input()


def maxify(grid, offset):
    heights = [offset for _ in range(7)]
    for i, row in enumerate(reversed(grid)):
        for j, c in enumerate(row):
            if c == "#":
                heights[j] = i + offset

    return heights


class DuplicateSpotter:
    def __init__(self):
        self.seen = {}

    def __call__(self, k, grid, jets, rock):
        if grid[0] in (["#" for _ in range(7)], ["~" for _ in range(7)]):
            key = "".join(jets) + "\n".join(rock)
            if key in self.seen:
                return self.seen[key]
            else:
                self.seen[key] = (k, len(grid))
