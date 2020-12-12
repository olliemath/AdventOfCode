import os

from day_12.solution import parse, follow


TEST = ["F10\n", "N3\n", "F7\n", "R90\n", "F11\n"]


def test_follow():
    assert follow(parse(TEST)) == 25
