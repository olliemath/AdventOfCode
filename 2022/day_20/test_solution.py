from .solution import parse, part1, part2


data = """
1
2
-3
3
-2
0
4
"""


def test_part1():
    assert part1(parse(data)) == 3


def test_part2():
    assert part2(parse(data)) == 1623178306
