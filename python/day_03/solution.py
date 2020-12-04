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


def solve(input):
    print(path_count(get_grid(input)))
