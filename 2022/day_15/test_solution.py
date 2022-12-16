import itertools
from .solution import manhatten, parse, part1, part2


data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def test_solution():
    assert part1(list(parse(data)), 10) == 26

    for y in range(20):
        assert part1(list(parse(data)), y) == part1_slow(list(parse(data)), y)

    assert part2(list(parse(data)), 20) == 56000011


def part1_slow(input, y):
    # Here for testing purposes!
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
