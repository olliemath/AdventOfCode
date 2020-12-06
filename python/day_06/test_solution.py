import os

from day_06.solution import parse, num_yeses_any, num_yeses_all


TEST_GROUPS = [
    "abc\n",
    "\n",
    "a\n",
    "b\n",
    "c\n",
    "\n",
    "ab\n",
    "ac\n",
    "\n",
    "a\n",
    "a\n",
    "a\n",
    "a\n",
    "\n",
    "b\n",
]


def test_parse():
    parsed = list(parse(TEST_GROUPS))
    assert [len(g) for g in parsed] == [1, 3, 2, 4, 1]


def test_num_yeses_any():
    assert num_yeses_any(parse(TEST_GROUPS)) == 11


def test_num_yeses_all():
    assert num_yeses_all(parse(TEST_GROUPS)) == 6
