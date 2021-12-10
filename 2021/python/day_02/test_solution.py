from .solution import parse, solve


data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def test_solution():
    assert solve(parse(data)) == (150, 900)
