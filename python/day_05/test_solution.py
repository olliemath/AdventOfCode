import os

from day_05.solution import parse_boarding_pass, parse_boarding_passes


def test_parse_boarding_pass():
    pass_ = "FBFBBFFRLR"
    assert parse_boarding_pass(pass_) == (44, 5, 357)


def test_parse_boarding_passes():
    passes = ["BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"]
    expected = [(70, 7, 567), (14, 7, 119), (102, 4, 820)]
    assert parse_boarding_passes(passes) == expected
