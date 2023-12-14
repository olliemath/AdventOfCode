from __future__ import annotations

from .solution import parse, part1, part2, solve_quadratic

data = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_solution():
    assert part1(parse(data)) == 288
    assert part2(parse(data)) == 71503



def test_solve_quadratic():
    assert solve_quadratic(7, 9) == (2, 5)
    assert solve_quadratic(15, 40) == (4, 11)
    assert solve_quadratic(30, 200) == (11, 19)
