from .solution import parse, solve


data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_solution():
    assert solve(parse(data)) == (4361, 467835)
