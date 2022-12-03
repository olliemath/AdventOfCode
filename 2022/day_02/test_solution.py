from .solution import parse, solve


data = """
A Y
B X
C Z
"""


def test_solution():
    assert solve(parse(data)) == (15, 12)
