from __future__ import annotations


def parse(data):
    rows = data.strip().split("\n")
    result = []
    for row in rows:
        rp, rv = row.split(" @ ")
        rp = tuple(map(int, rp.split(", ")))
        rv = tuple(map(int, rv.split(", ")))
        result.append((rp, rv))
    return result


def solve(input):
    return part1(input), part2(input)


def part1(input, lower=200000000000000, upper=400000000000000):
    total = 0
    for i, l1 in enumerate(input):
        for l2 in input[i + 1 :]:
            if inter := interpoint(l1, l2):
                if lower <= inter[0] <= upper and lower <= inter[1] <= upper:
                    total += 1
    return total


def part2(input):
    # Refer to https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    # you can see that (p - q) x (r - s) = 0, because t == u.
    # If we weren't so lazy, we'd use Gaussian elimination to solve the system
    (x1, v1), (x2, v2), (x3, v3) = input[1:4]

    import numpy as np

    matrix = np.array(
        [
            [-(v1[1] - v2[1]), v1[0] - v2[0], 0, x1[1] - x2[1], -(x1[0] - x2[0]), 0],
            [-(v1[1] - v3[1]), v1[0] - v3[0], 0, x1[1] - x3[1], -(x1[0] - x3[0]), 0],
            [0, -(v1[2] - v2[2]), v1[1] - v2[1], 0, x1[2] - x2[2], -(x1[1] - x2[1])],
            [0, -(v1[2] - v3[2]), v1[1] - v3[1], 0, x1[2] - x3[2], -(x1[1] - x3[1])],
            [-(v1[2] - v2[2]), 0, v1[0] - v2[0], x1[2] - x2[2], 0, -(x1[0] - x2[0])],
            [-(v1[2] - v3[2]), 0, v1[0] - v3[0], x1[2] - x3[2], 0, -(x1[0] - x3[0])],
        ]
    )

    offset = [
        (x1[1] * v1[0] - x2[1] * v2[0]) - (x1[0] * v1[1] - x2[0] * v2[1]),
        (x1[1] * v1[0] - x3[1] * v3[0]) - (x1[0] * v1[1] - x3[0] * v3[1]),
        (x1[2] * v1[1] - x2[2] * v2[1]) - (x1[1] * v1[2] - x2[1] * v2[2]),
        (x1[2] * v1[1] - x3[2] * v3[1]) - (x1[1] * v1[2] - x3[1] * v3[2]),
        (x1[2] * v1[0] - x2[2] * v2[0]) - (x1[0] * v1[2] - x2[0] * v2[2]),
        (x1[2] * v1[0] - x3[2] * v3[0]) - (x1[0] * v1[2] - x3[0] * v3[2]),
    ]

    x = np.linalg.solve(matrix, offset)
    return int(sum(x[:3]))


def interpoint(l1, l2):
    (px1, py1, _), (vx1, vy1, _) = l1
    (px2, py2, _), (vx2, vy2, _) = l2

    # px1 + t vx1 = px2 + s vx2
    # py1 + t vy1 = py2 + s vy2
    # => vy2 / vx2 (px1 + t vx1) = vy2.px2/vx2 + s vy2
    # => a.px1 - py1 + t (a.vx1 - vy1) = a.px2 - py2
    # => t = a.(px2 - px1) - (py2 - py1) ) / (a.vx1 - vy1)

    try:
        a = vy2 / vx2
        t = (a * (px2 - px1) - (py2 - py1)) / (a * vx1 - vy1)
        s = (px1 - px2 + t * vx1) / vx2
    except ZeroDivisionError:
        return None

    if t < 0 or s < 0:
        return None

    x = px1 + t * vx1
    y = py1 + t * vy1

    return (x, y)
