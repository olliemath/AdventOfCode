from __future__ import annotations

from .solution import parse, solve

data = """
.....
.S-7.
.|.|.
.L-J.
.....
"""


def test_solution():
    assert solve(parse(data)) == (4, 1)


data2 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

data3 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


def test_solution2():
    assert solve(parse(data2))[1] == 4


def test_solution3():
    assert solve(parse(data3))[1] == 8
