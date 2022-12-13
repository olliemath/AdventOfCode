from .solution import parse, solve


data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def test_solution():
    assert solve(parse(data)) == (31, 29)
