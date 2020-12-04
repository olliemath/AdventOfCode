import os

from day_01.solution import parse_expenses, find_tuple, get_prod


FIXDIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "fixtures"
)


def test_parse_expenses():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        expenses = list(parse_expenses(f))

    assert len(expenses) == 6


def test_find_tuple():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        expenses = list(parse_expenses(f))

    assert sorted(find_tuple(expenses, 2)) == sorted((1721, 299))
    assert sorted(find_tuple(expenses, 3)) == sorted((979, 366, 675))


def test_get_prod():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        lines = f.readlines()

    assert get_prod(lines, 2) == 514579
    assert get_prod(lines, 3) == 241861950
