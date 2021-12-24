import math


def parse(input):
    res = []
    chunks = input.strip().split("\n\n")
    for chunk in chunks:
        chunk = chunk.strip().split("\n")[1:]
        chunk = [list(map(int, line.split(","))) for line in chunk]
        res.append(chunk)

    return res


def solve(input):
    points, offsets = compute(input)

    biggest = 0
    for a in offsets:
        for b in offsets:
            biggest = max(biggest, sum(abs(a[i] - b[i]) for i in range(3)))

    return len(points), biggest


def compute(input):
    sol = [(input[0], (0, 0, 0), get_deltas(input[0]))]

    to_match = []
    missed = [(i, get_deltas(i)) for i in input[1:]]
    current = 0

    while missed:
        to_match, missed = missed, []

        for chunk, deltas in to_match:
            matched = quick_match_chunk(
                sol[current][0], sol[current][2], chunk, deltas
            )
            if matched:
                sol.append(matched)
            else:
                missed.append((chunk, deltas))

        current += 1

    points = set(map(tuple, sol[0][0]))
    offsets = [sol[0][1]]
    for chunk, offset, _ in sol[1:]:
        points.update(map(tuple, chunk))
        offsets.append(offset)

    return points, offsets


def match_chunk(f, c):
    fs = set(map(tuple, f))

    # Any orientation and offset
    for orient in rotate(c):
        # See if they overlap
        for x, y, z in f:
            # Make the two overlap and see if 12 others match
            for p, q, r in orient:
                dp, dq, dr = x - p, y - q, z - r

                matches = 0
                for pp, qq, rr in orient:
                    if (pp + dp, qq + dq, rr + dr) in fs:
                        matches += 1
                        if matches >= 12:
                            return [
                                (a + dp, b + dq, c + dr) for a, b, c in orient
                            ], (dp, dq, dr)


def get_deltas(c):
    dists = set()
    for (x, y, z) in c:
        for (p, q, r) in c:
            if (x, y, z) != (p, q, r):
                dists.add(
                    math.sqrt((x-p) ** 2 + (y-q) ** 2 + (z-r)**2)
                )
    return dists


def quick_match_chunk(f, fdeltas, c, cdeltas):
    # This is a bit of a hack, but only do an expensive loop through all
    # possible rotations/shifts if deltas overlap to a significant degree
    if len(fdeltas.intersection(cdeltas)) < 66:  # 12 * 11 / 2
        return None
    match = match_chunk(f, c)
    if match:
        return match + (cdeltas,)


def rotate(chunk):
    new = [[] for _ in range(24)]
    for point in chunk:
        for i, r in enumerate(rotations24(point)):
            new[i].append(r)

    return new


def rot90(point, n, axis):
    # Rotate about the axis by 90 degrees n times
    to_rotate = point[:axis] + point[axis+1:]
    for _ in range(n):
        to_rotate = [-to_rotate[1], to_rotate[0]]

    if axis == 0:
        return [point[0], *to_rotate]
    elif axis == 1:
        return [to_rotate[0], point[1], to_rotate[1]]
    else:
        return [*to_rotate, point[2]]


def rotations4(point, axis):
    for n in range(4):
        yield rot90(point, n, axis)


def rotations24(point):
    """List all 24 rotations of the given space"""
    # imagine shape is pointing in axis 0 (up)

    # 4 rotations about axis 0
    yield from rotations4(point, axis=0)

    # rotate 180 about axis 1, now shape is pointing down in axis 0
    # 4 rotations about axis 0
    yield from rotations4(rot90(point, 2, axis=1), axis=0)

    # rotate 90 or 270 about axis 1, now shape is pointing in axis 2
    # 8 rotations about axis 2
    yield from rotations4(rot90(point, 1, axis=1), axis=2)
    yield from rotations4(rot90(point, 3, axis=1), axis=2)

    # rotate about axis 2, now shape is pointing in axis 1
    # 8 rotations about axis 1
    yield from rotations4(rot90(point, 1, axis=2), axis=1)
    yield from rotations4(rot90(point, 3, axis=2), axis=1)
