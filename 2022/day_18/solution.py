def parse(data):
    return [
        tuple(map(int, line.strip().split(",")))
        for line in data.strip().split("\n")
    ]


def solve(input):
    bounds = [
        (min(p[x] for p in input) - 1, max(p[x] for p in input) + 2)
        for x in range(3)
    ]
    grid = [
        [
            ["." for _ in range(*bounds[0])]
            for _ in range(*bounds[1])
        ]
        for _ in range(*bounds[2])
    ]
    x0, y0, z0 = [b[0] for b in bounds]
    for x, y, z in input:
        grid[z - z0][y - y0][x - x0] = "#"

    return surface(grid), outer_surface(grid)


def surface(grid):
    total = 0
    for i, plane in enumerate(grid):
        for j, row in enumerate(plane):
            for k, point in enumerate(row):
                if point == "#":
                    for other in surrounding(grid, i, j, k):
                        if get(grid, *other) == ".":
                            total += 1

    return total


def outer_surface(grid):
    surface = 0
    queue = [(0, 0, k) for k in range(len(grid[0][0]))]
    while queue:
        i, j, k = queue.pop()
        if grid[i][j][k] == "~":
            continue
        grid[i][j][k] = "~"

        for coords in surrounding(grid, i, j, k):
            point = get(grid, *coords)
            if point == ".":
                queue.append(coords)
            elif point == "#":
                surface += 1

    return surface


def get(grid, i, j, k):
    return grid[i][j][k]


def surrounding(grid, i, j, k):
    for dx in (-1, 1):
        if 0 <= i + dx < len(grid):
            yield (i + dx, j, k)
        if 0 <= j + dx < len(grid[0]):
            yield (i, j + dx, k)
        if 0 <= k + dx < len(grid[0][0]):
            yield (i, j, k + dx)


def printgrid(grid):
    for plane in grid:
        print("\n" + "\n".join("".join(row) for row in plane))
