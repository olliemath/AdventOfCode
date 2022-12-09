from .solution import parse, solve


data = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


def test_solution():
    assert solve(parse(data)) == (13, 1)


def test_solution2():
    data = """
    R 5
    U 8
    L 8
    D 3
    R 17
    D 10
    L 25
    U 20
    """

    assert solve(parse(data))[1] == 36
