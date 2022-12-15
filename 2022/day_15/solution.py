import itertools
import re


def parse(data):
    rex = re.compile(r"^.+x=([-0-9]+), y=([-0-9]+).+x=([-0-9]+), y=([-0-9]+)$")

    for line in data.strip().split("\n"):
        sx, sy, bx, by = rex.match(line).groups()
        yield (int(sx), int(sy)), (int(bx), int(by))


def solve(input):
    input = list(input)
    return (
        part1(input, 2_000_000),
        part2(input, 4_000_000),
    )


def part1(input, y):
    segments = []
    ocupado = set()

    for sensor, beacon in input:
        radius = manhatten(sensor, beacon)
        sx, sy = sensor
        bx, by = beacon

        overlap = radius - abs(sy - y)
        if overlap >= 0:
            segments = append_segment(
                segments, (sx - overlap, sx + overlap, 1)
            )

        if by == y:
            ocupado.add(bx)
        if sy == y:
            ocupado.add(sx)

    return sum(1 + end - start for start, end, _ in segments) - len(ocupado)


def part2(input, bound):
    # Let u = x + y and v = x - y, let's rotate into that coordinate system
    # This changes the manhatten distance to the L-infinity distance (cool!)
    input = [(rotate(*s), rotate(*b)) for s, b in input]

    # Now all the diamons are squares - lets start with the left-most square
    # and build a "wave-front" which should proceed across the grid covering
    # everything until we hit our beacon point.
    # For each new square the left-most edge must be the largest possible
    # left-most edge
    input = sorted(input, key=lambda pair: pair[0][0] - linf(*pair))

    # The big (x, y) grid we're checking is a (u, v) diamond with
    # 0 <= u + v <= 2 * bound, -bound <= u - v <= bound
    # segments = [(0, 0, -1)]
    segments = [(0, 0, -1)]

    for sensor, beacon in input:
        radius = linf(sensor, beacon)
        # Check no points are to the right of the wave and left of this square
        u_outer = sensor[0] - radius - 1
        for v in range(
            max(sensor[1] - radius, -u_outer, u_outer - 2 * bound),
            min(sensor[1] + radius + 1, u_outer, 2 * bound - u_outer),
        ):
            # Check for points to the left
            for sv_lower, sv_upper, su in segments:
                if sv_lower <= v <= sv_upper:
                    if su < u_outer:
                        return result(u_outer, v)
                    break
            else:
                # no segment to the left of this v
                return result(u_outer, v)

        # Now we need to update the segments
        u_upper = sensor[0] + radius
        v_lower = sensor[1] - radius
        v_upper = sensor[1] + radius
        segments = append_segment(segments, (v_lower, v_upper, u_upper))


def append_segment(segments, segment):
    to_process = [segment]
    new_segments = segments

    while to_process:
        segments, new_segments = new_segments, []

        vl, vu, u = segment = to_process.pop()
        for k, other in enumerate(segments):
            other_vl, other_vu, other_u = other
            # We completely cover the other segment
            if vl <= other_vl and vu >= other_vu:
                if u >= other_u:
                    continue  # no need for this segment
                else:
                    # The middle chunk is covered by the old segment
                    new_segments.extend(segments[k:])
                    if vl <= other_vl - 1:
                        to_process.append((vl, other_vl - 1, u))
                    if other_vu + 1 <= vu:
                        to_process.append((other_vu + 1, vu, u))
                    break

            # Other segment completely covers us
            elif other_vl <= vl and other_vu >= vu:
                if u >= other_u:
                    if other_vl <= vl - 1:
                        to_process.append((other_vl, vl - 1, other_u))
                    if vu + 1 <= other_vu:
                        to_process.append((vu + 1, other_vu, other_u))
                    continue  # TODO: could append and break here
                else:
                    new_segments.extend(segments[k:])
                    break

            elif vl <= other_vl and vu >= other_vl:
                if u >= other_u:
                    if vu + 1 <= other_vu:
                        to_process.append((vu + 1, other_vu, other_u))
                    continue
                else:
                    new_segments.append(other)
                    if vl <= other_vl - 1:
                        to_process.append((vl, other_vl - 1, u))

            elif vl <= other_vu and vu >= other_vu:
                if u >= other_u:
                    if other_vl <= vl - 1:
                        to_process.append((other_vl, vl - 1, other_u))
                    continue
                else:
                    new_segments.append(other)
                    if other_vu + 1 <= vu:
                        to_process.append((other_vu + 1, vu, u))
            else:
                new_segments.append(other)  # doesn't overlap

        else:
            new_segments.append(segment)

    return sorted(new_segments)


def manhatten(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def linf(x, y):
    return max(abs(x[0] - y[0]), abs(x[1] - y[1]))


def rotate(x, y):
    return x + y, x - y


def unrotate(u, v):
    return (u + v) // 2, (u - v) // 2


def result(u, v):
    x, y = unrotate(u, v)
    return 4_000_000 * x + y


def part1_slow(input, y):
    # Basic way to check we have the right answer!
    biggest_radius = max(manhatten(s, b) for s, b in input)

    xmin = min(p[0] for p in itertools.chain(*input)) - biggest_radius
    xmax = max(p[0] for p in itertools.chain(*input)) + biggest_radius
    ymin = min(p[1] for p in itertools.chain(*input)) - biggest_radius
    ymax = max(p[1] for p in itertools.chain(*input)) + biggest_radius

    grid = [
        ["." for _ in range(xmin, xmax + 1)] for _ in range(ymin, ymax + 1)
    ]
    for (sx, sy), (bx, by) in input:
        grid[sy - ymin][sx - xmin] = "S"
        grid[by - ymin][bx - xmin] = "B"

        radius = manhatten((sx, sy), (bx, by))
        for dy in range(-radius, radius + 1):
            for dx in range(-radius + abs(dy), radius - abs(dy) + 1):
                if grid[sy - ymin + dy][sx - xmin + dx] == ".":
                    grid[sy - ymin + dy][sx - xmin + dx] = "#"

    # printgrid(grid)
    return grid[y - ymin].count("#")
