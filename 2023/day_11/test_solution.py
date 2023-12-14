from __future__ import annotations

from .solution import expand, parse, part1, shortest_path

data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_shortest_path():
    universe = expand(parse(data))

    pairs = {v: k for k, v in universe.items()}
    assert shortest_path(pairs[5], pairs[9]) == 9
    assert shortest_path(pairs[1], pairs[7]) == 15
    assert shortest_path(pairs[3], pairs[6]) == 17
    assert shortest_path(pairs[8], pairs[9]) == 5


def test_solution():
    assert part1(parse(data)) == 374


def test_solution_part2():
    assert part1(parse(data), factor=10) == 1030
    assert part1(parse(data), factor=100) == 8410
