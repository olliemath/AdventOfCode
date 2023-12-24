from __future__ import annotations

from .solution import parse, part2

data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_solution():
    assert part2(parse(data), 6) == 16
    assert part2(parse(data), 10) == 50
    assert part2(parse(data), 50) == 1594
    assert part2(parse(data), 100) == 6536
    assert part2(parse(data), 500) == 167004
    assert part2(parse(data), 1000) == 668697
    assert part2(parse(data), 5000) == 16733044
