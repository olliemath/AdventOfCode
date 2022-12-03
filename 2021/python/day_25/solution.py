def parse(input):
    return [list(r) for r in input.strip().split("\n")]


def solve(input):
    prev = None
    new = input
    k = 0

    while prev != new:
        k += 1
        prev, new = new, step(new)

    return k


def step(grid):
    new_grid = []

    # East moving herd
    for row in grid:
        new_row = list(row)
        for i, c in enumerate(row):
            if c == ">" and row[(i+1) % len(row)] == ".":
                new_row[(i+1) % len(row)] = ">"
                new_row[i] = "."
        new_grid.append(new_row)
    # import pdb; pdb.set_trace()

    # South moving herd
    for i in range(len(grid[0])):
        new_col = [r[i] for r in new_grid]
        for j, row in enumerate(new_grid):
            if row[i] == "v" and new_grid[(j+1) % len(new_grid)][i] == ".":
                new_col[(j+1) % len(new_grid)] = "v"
                new_col[j] = "."

        for j, c in enumerate(new_col):
            new_grid[j][i] = c

    return new_grid
