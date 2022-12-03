from .solution import parse, solve


data = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_solution():
    assert solve(parse(data)) == (24_000, 45_000)
