from .solution import parse, score, solve, view


data = """
30373
25512
65332
33549
35390
"""


def test_solution():
    assert solve(parse(data)) == (21, 8)


def test_score():
    parsed = parse(data)

    assert view(parsed, 1, 2) == (1, 2, 1, 2)
    assert view(parsed, 3, 2) == (2, 2, 2, 1)
    assert score(parsed, 1, 2) == 4
    assert score(parsed, 3, 2) == 8
