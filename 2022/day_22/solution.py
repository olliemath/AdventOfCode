import re


def parse(data):
    grid_string, inst_string = data.split("\n\n")
    instructions = []
    for num, dirs in re.findall(r"([0-9]+)([LR]+)?", inst_string):
        instructions.append(int(num))
        for d in dirs:
            instructions.append(d)

    grid = [line for line in grid_string.split("\n") if line.strip()]
    longest = max(len(line) for line in grid)
    grid = [
        line + "".join(" " for _ in range(longest - len(line)))
        for line in grid
    ]

    return grid, instructions


def solve(input):
    return part1(input), part2(input)


def part1(input):
    grid, instructions = input
    pos = (0, 0)
    dir = (1, 0)

    # Move to first square
    pos = move(grid, pos, dir, [(pos, facing(dir)[0])])
    path = [(pos, facing(dir)[0])]

    for ins in instructions:
        if isinstance(ins, int):
            pos = move(grid, pos, (dir[0] * ins, dir[1] * ins), path)
        else:
            if ins == "L":
                dir = (-dir[1], dir[0])
                path[-1] = (path[-1][0], facing(dir)[0])
            elif ins == "R":
                dir = (dir[1], -dir[0])
                path[-1] = (path[-1][0], facing(dir)[0])

    printgrid(grid, path)
    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing(dir)[1]


def part2(input_, size=50):
    """
            ----
           *1111#
           *1111#
           *1111#
    ----****1111#
    222233334444~
    222233334444~
    222233334444~
    222233334444~~~~
    ....    55556666#
            55556666#
            55556666#
            55556666#
            ....
    """
    grid, instructions = input_

    # Let's split the grid out into faces
    faces = []
    for k in range(2):
        faces.append([grid[i][(k+1) * size:(k+2) * size] for i in range(size)])
    faces.append([grid[i + size][size:2 * size] for i in range(size)])
    for k in range(2):
        faces.append(
            [grid[i + 2 * size][k * size:(k+1) * size] for i in range(size)]
        )
    faces.append([grid[i + 3 * size][0:size] for i in range(size)])

    # Logic used for the test grid - nasty hard coding!
    # faces.append([grid[i][2 * size:3 * size] for i in range(size)])
    # for n in range(3):
    #     faces.append([
    #         grid[i + size][n * size:(n + 1) * size] for i in range(size)
    #     ])
    # for n in range(2):
    #     faces.append([
    #         grid[i + 2 * size][(n + 2) * size:(n + 3) * size]
    #         for i in range(size)
    #     ])
    # mappings = {
    #     "<": {
    #         1: lambda pos: (3, (pos[1], 0), "v"),
    #         2: lambda pos: (6, (size - 1 - pos[1], size - 1), "^"),
    #         3: lambda pos: (2, (size - 1, pos[1]), "<"),
    #         4: lambda pos: (3, (size - 1, pos[1]), "<"),
    #         5: lambda pos: (3, (size - 1 - pos[1], size - 1), "^"),
    #         6: lambda pos: (5, (size - 1, pos[1]), "<"),
    #     },
    #     ">": {
    #         1: lambda pos: (6, (size - 1, size - 1 - pos[1]), "<"),
    #         2: lambda pos: (3, (0, pos[1]), ">"),
    #         3: lambda pos: (4, (0, pos[1]), ">"),
    #         4: lambda pos: (6, (size - 1 - pos[1], 0), "v"),
    #         5: lambda pos: (6, (0, pos[1]), ">"),
    #         6: lambda pos: (1, (size - 1, size - 1 - pos[1]), "<"),
    #     },
    #     "v": {
    #         1: lambda pos: (4, (pos[0], 0), "v"),
    #         2: lambda pos: (5, (size - 1 - pos[0], size - 1), "^"),
    #         3: lambda pos: (5, (0, size - 1 - pos[0]), ">"),
    #         4: lambda pos: (5, (pos[0], 0), "v"),
    #         5: lambda pos: (2, (size - 1 - pos[0], size - 1), "^"),
    #         6: lambda pos: (2, (0, size - 1 - pos[0]), ">"),
    #     },
    #     "^": {
    #         1: lambda pos: (2, (size - 1 - pos[0], 0), "v"),
    #         2: lambda pos: (1, (size - 1 - pos[0], 0), "v"),
    #         3: lambda pos: (1, (0, pos[0]), ">"),
    #         4: lambda pos: (1, (pos[0], size - 1), "^"),
    #         5: lambda pos: (4, (pos[0], size - 1), "^"),
    #         6: lambda pos: (4, (size - 1 - pos[0], size - 1), "<"),
    #     },
    # }

    mappings = {
        "<": {
            1: lambda pos: (4, (0, size - 1 - pos[1]), ">"),
            2: lambda pos: (1, (size - 1, pos[1]), "<"),
            3: lambda pos: (4, (pos[1], 0), "v"),
            4: lambda pos: (1, (0, size - 1 - pos[1]), ">"),
            5: lambda pos: (4, (size - 1, pos[1]), "<"),
            6: lambda pos: (1, (pos[1], 0), "v"),
        },
        ">": {
            1: lambda pos: (2, (0, pos[1]), ">"),
            2: lambda pos: (5, (size - 1, size - 1 - pos[1]), "<"),
            3: lambda pos: (2, (pos[1], size - 1), "^"),
            4: lambda pos: (5, (0, pos[1]), ">"),
            5: lambda pos: (2, (size - 1, size - 1 - pos[1]), "<"),
            6: lambda pos: (5, (pos[1], size - 1), "^"),
        },
        "v": {
            1: lambda pos: (3, (pos[0], 0), "v"),
            2: lambda pos: (3, (size - 1, pos[0]), "<"),
            3: lambda pos: (5, (pos[0], 0), "v"),
            4: lambda pos: (6, (pos[0], 0), "v"),
            5: lambda pos: (6, (size - 1, pos[0]), "<"),
            6: lambda pos: (2, (pos[0], 0), "v"),
        },
        "^": {
            1: lambda pos: (6, (0, pos[0]), ">"),
            2: lambda pos: (6, (pos[0], size - 1), "^"),
            3: lambda pos: (1, (pos[0], size - 1), "^"),
            4: lambda pos: (3, (0, pos[0]), ">"),
            5: lambda pos: (3, (pos[0], size - 1), "^"),
            6: lambda pos: (4, (pos[0], size - 1), "^"),
        },
    }

    path = [(1, (0, 0), ">")]
    face, (x, y), arrow = path[0]
    dir = IFACING[arrow]

    # Move to first square
    for ins in instructions:
        # printgrid2(grid, path, size)
        if isinstance(ins, str):
            if ins == "L":
                dir = (dir[1], -dir[0])
                path[-1] = (path[-1][0], path[-1][1], FACING[dir])
            elif ins == "R":
                dir = (-dir[1], dir[0])
                path[-1] = (path[-1][0], path[-1][1], FACING[dir])
            continue

        for _ in range(ins):
            if dir[0]:
                d = dir[0]

                xnew = x + d
                if xnew < 0:
                    fnew, (xnew, ynew), dnew = mappings["<"][face]((x, y))
                elif xnew >= size:
                    fnew, (xnew, ynew), dnew = mappings[">"][face]((x, y))
                else:
                    dnew = FACING[dir]
                    ynew = y
                    fnew = face

                char = faces[fnew-1][ynew][xnew]

                if char == "#":
                    break
                else:
                    face, x, y, dir = fnew, xnew, ynew, IFACING[dnew]
                    path.append((face, (x, y), dnew))

            else:
                d = dir[1]
                ynew = y + d
                if ynew < 0:
                    fnew, (xnew, ynew), dnew = mappings["^"][face]((x, y))
                elif ynew >= size:
                    fnew, (xnew, ynew), dnew = mappings["v"][face]((x, y))
                else:
                    dnew = FACING[dir]
                    xnew = x
                    fnew = face

                char = faces[fnew-1][ynew][xnew]
                if char == "#":
                    break
                else:
                    face, x, y, dir = fnew, xnew, ynew, IFACING[dnew]
                    path.append((face, (x, y), dnew))

    printgrid2(grid, path, size)

    # This logic is used for the test grid - nasty hard coding!
    # if face == 1:
    #     rx = x + 2 * size
    #     ry = y
    # elif face in (2, 3, 4):
    #     rx = x + (face - 2) * size
    #     ry = y + size
    # else:
    #     rx = x + (face - 3) * size
    #     ry = y + 2 * size

    if face in (1, 2):
        rx = x + face * size
        ry = y
    elif face == 3:
        rx = x + size
        ry = y + size
    elif face in (4, 5):
        rx = x + (face - 4) * size
        ry = y + 2 * size
    else:
        rx = x
        ry = y + 3 * size

    return 1000 * (ry + 1) + 4 * (rx + 1) + facing(dir)[1]


def move(grid, pos, delta, path):
    x, y = pos
    dx, dy = delta
    if dx:
        d, dx = dx // abs(dx), abs(dx)
        line = grid[y]
        for _ in range(dx):
            xnew, char = get_next(line, x, d)
            if char == "#":
                break
            else:
                x = xnew
                path.append(((x, y), path[-1][1]))
    else:
        d, dy = dy // abs(dy), abs(dy)
        line = [grid[k][x] for k in range(len(grid))]
        for _ in range(dy):
            ynew, char = get_next(line, y, -d)
            if char == "#":
                break
            else:
                y = ynew
                path.append(((x, y), path[-1][1]))

    return x, y


def get_next(line, p, d):
    new_p = (p + d) % len(line)
    if all(c == " " for c in line):
        raise RuntimeError("'" + line + "'")

    while line[new_p] == " ":
        new_p = (new_p + d) % len(line)

    return new_p, line[new_p]


def facing(dir):
    if dir == (1, 0):
        return ">", 0
    elif dir == (0, 1):
        return "v", 1
    elif dir == (-1, 0):
        return "<", 2
    else:
        return "^", 3


def printgrid(grid, path):
    splitgrid = [list(line) for line in grid]
    for pos, arrow in path:
        splitgrid[pos[1]][pos[0]] = arrow
    print()
    for line in splitgrid:
        print("".join(line))


def printgrid2(grid, path, size):
    splitgrid = [list(line) for line in grid]

    # This logic is used for the test grid - nasty hard coding!
    # for face, pos, arrow in path:
    #     if face == 1:
    #         x = pos[0] + 2 * size
    #         y = pos[1]
    #     elif face in (2, 3, 4):
    #         x = pos[0] + (face - 2) * size
    #         y = pos[1] + size
    #     else:
    #         x = pos[0] + (face - 3) * size
    #         y = pos[1] + 2 * size

    #     splitgrid[y][x] = arrow
    # print()
    # for line in splitgrid:
    #     print("".join(line))

    splitgrid = [list(line) for line in grid]
    for face, (x, y), arrow in path:
        if face in (1, 2):
            rx = x + face * size
            ry = y
        elif face == 3:
            rx = x + size
            ry = y + size
        elif face in (4, 5):
            rx = x + (face - 4) * size
            ry = y + 2 * size
        else:
            rx = x
            ry = y + 3 * size

        splitgrid[ry][rx] = arrow
    print()
    for line in splitgrid:
        print("".join(line))


FACING = {
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
    (0, -1): "^",
}
IFACING = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}


def unconform_coords(face, x, y):
    pass
