from __future__ import annotations

from .solution import interpoint, parse, part1, part2

data = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


def test_interpoint():
    x, y = interpoint(((19, 13, 30), (-2, 1, -2)), ((18, 19, 22), (-1, -1, -2)))
    assert (round(x, 3), round(y, 3)) == (14.333, 15.333)

    inter = interpoint(((19, 13, 30), (-2, 1, -2)), ((20, 19, 15), (1, -5, -3)))
    assert inter is None


def test_solution():
    assert part1(parse(data), 7, 27) == 2
    assert part2(parse(data)) == 47
