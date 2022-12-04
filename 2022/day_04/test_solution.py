from .solution import overlap, parse, solve


data = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def test_solution():
    assert solve(parse(data)) == (2, 4)


def test_overlap():
    assert overlap((1, 3), (3, 5))
    assert overlap((1, 6), (3, 5))
    assert overlap((3, 5), (1, 3))
    assert overlap((3, 5), (1, 6))
    assert not overlap((1, 2), (3, 5))
    assert not overlap((3, 5), (1, 2))
