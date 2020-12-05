PATHS = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def get_grid(lines):
    return [l.strip() for l in lines]


def path_count(grid, x=3, y=1):
    px, py = 0, 0

    x_len = len(grid[0])
    y_len = len(grid)
    count = 0

    while True:
        px = (px + x) % x_len
        py += y

        if py >= y_len:
            break

        if grid[py][px] == "#":
            count += 1

    return count


def path_product(grid, paths=None):
    if paths is None:
        paths = PATHS

    product = 1
    for x, y in paths:
        product *= path_count(grid, x=x, y=y)

    return product


def solve(input):
    print(path_product(get_grid(input)))
