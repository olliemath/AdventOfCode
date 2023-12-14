from __future__ import annotations

from .solution import cycle, parse, part1, part2

data = """
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""


def test_cycle():
    grid = parse(data)

    grid = cycle(grid)
    assert grid == parse("""
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
    """)

    grid = cycle(grid)
    assert grid == parse("""
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
    """)

    grid = cycle(grid)
    assert grid == parse("""
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
    """)


def test_solution():
    assert part1(parse(data)) == 136
    assert part2(parse(data)) == 64
