from day_06.solution import parse, compute, solve


data = "3,4,3,1,2"


def test_compute():
    assert compute(parse(data), 18) == 26


def test_solve():
    assert solve(parse(data)) == (5934, 26984457539)
