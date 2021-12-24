from day_21.solution import compute, compute2, parse

data = """Player 1 starting position: 4
Player 2 starting position: 8"""


def test_solve():
    assert compute(parse(data)) == 739785
    assert compute2(parse(data)) == (444356092776315, 341960390180808)
