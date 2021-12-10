from day_07.solution import parse, solve


data = "16,1,2,0,4,2,7,1,2,14"


def test_solve():
    assert solve(parse(data)) == (37, 168)
