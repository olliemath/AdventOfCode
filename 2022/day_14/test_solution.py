from .solution import parse, solve


data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def test_solution():
    assert solve(parse(data)) == (24, 93)
