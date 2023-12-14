from __future__ import annotations

from .solution import parse, part1, part2

data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def test_solution():
    assert part1(parse(data)) == 405
    assert part2(parse(data)) == 400
