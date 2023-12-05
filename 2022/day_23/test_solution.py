from .solution import parse, part1, part2


data = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""


def test_part1():
    assert part1(parse(data)) == 110


def test_part2():
    assert part2(parse(data)) == 20
