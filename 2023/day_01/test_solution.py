from __future__ import annotations

from .solution import parse, solve

data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def test_solution():
    assert solve(parse(data))[0] == 142


data2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def test_solution2():
    assert solve(parse(data2))[1] == 281
