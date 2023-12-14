from __future__ import annotations

from .solution import parse, solve

data = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_solution():
    assert solve(parse(data)) == (114, 2)
