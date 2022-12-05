from .solution import parse, solve


data = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def test_parse():
    stacks, instructions = parse(data)
    assert stacks == [["Z", "N"], ["M", "C", "D"], ["P"]]
    assert instructions == [[1, 2, 1], [3, 1, 3], [2, 2, 1], [1, 1, 2]]


def test_solve():
    assert solve(parse(data)) == ("CMZ", "MCD")
