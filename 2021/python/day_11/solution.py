import curses


def parse(input):
    return [[int(c) for c in r] for r in input.strip().split("\n")]


def solve(input):
    return compute(input)


def compute(input):
    # stdscr = curses.initscr()
    # curses.noecho()
    # curses.cbreak()
    # curses.start_color()
    # stdscr.clear()

    flashed = 0
    all_flashed = None

    k = 0
    try:
        while all_flashed is None or k < 100:
            k += 1
            flashed_in_step = step(input)
            # print_grid(stdscr, input)

            if k <= 100:
                flashed += flashed_in_step

            if (
                all_flashed is None
                and flashed_in_step == len(input) * len(input[0])
            ):
                all_flashed = k

        # stdscr.getkey()
    finally:
        # curses.endwin()
        pass

    return flashed, all_flashed


def step(grid):
    for row in grid:
        for n, _ in enumerate(row):
            row[n] += 1

    flashed = set()
    to_flash = set()
    for n, row in enumerate(grid):
        for m, i in enumerate(row):
            if i > 9:
                to_flash.add((n, m))

    flash(grid, flashed, to_flash)

    for row in grid:
        for n, i in enumerate(row):
            if i > 9:
                row[n] = 0

    return len(flashed)


def flash(grid, flashed, to_flash):
    new_to_flash = set()
    flashed.update(to_flash)

    for n, m in to_flash:

        neighbours = [
            (n-1, m-1), (n-1, m), (n-1, m+1),
            (n, m-1), (n, m+1),
            (n+1, m-1), (n+1, m), (n+1, m+1),
        ]
        neighbours = [(n, m) for n, m in neighbours if n >= 0 and m >= 0]

        for j, k in neighbours:
            try:
                grid[j][k] += 1
            except IndexError:
                continue
            if grid[j][k] > 9 and (j, k) not in flashed:
                new_to_flash.add((j, k))

    if new_to_flash:
        flash(grid, flashed, new_to_flash)


def print_grid(stdscr, grid):
    import time
    time.sleep(0.1)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    for i, row in enumerate(grid):
        for j, num in enumerate(row):
            if num > 0:
                stdscr.addstr(i+3, j+6, str(num), curses.color_pair(1))
            else:
                stdscr.addstr(i+3, j+6, str(num), curses.color_pair(2))

    stdscr.refresh()
