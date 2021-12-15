def parse(input):
    grid, folds = input.split("\n\n")
    grid = {
        tuple(map(int, line.split(",")))
        for line in grid.strip().split("\n")
    }
    folds = [
        line.split()[2].split("=")
        for line in folds.strip().split("\n")
    ]

    return grid, folds


def solve(input):
    grid, folds = input
    output = display_grid(compute(grid, folds))
    return len(fold(grid, folds[0])), output


def compute(grid, folds):
    for f in folds:
        grid = fold(grid, f)
    return grid


def display_grid(grid):
    xx = max(x for x, y in grid)
    yy = max(y for x, y in grid)

    to_print = ["\n"]
    for y in range(yy + 1):
        for x in range(xx + 1):
            if (x, y) in grid:
                to_print.append("#")
            else:
                to_print.append(" ")
        to_print.append("\n")

    return "".join(to_print)


def fold(grid, fold):
    dir, pos = fold
    pos = int(pos)
    if dir == "x":
        return fold_left(grid, pos)
    return fold_up(grid, pos)


def fold_up(input, line):
    output = set()
    for x, y in input:
        if y < line:
            output.add((x, y))
        elif y > line:
            output.add((x, 2*line - y))
    return output


def fold_left(input, line):
    output = set()
    for x, y in input:
        if x < line:
            output.add((x, y))
        elif x > line:
            output.add((2*line - x, y))
    return output
