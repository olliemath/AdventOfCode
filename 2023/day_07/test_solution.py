from __future__ import annotations

from .solution import parse, solve

data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_solution():
    assert solve(parse(data)) == (6440, 5905)
