import os

from day_03.solution import get_grid, path_count, path_product


FIXDIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "fixtures"
)


def test_path_count():

    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        grid = get_grid(f)

    assert path_count(grid) == 7


def test_path_product():

    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        grid = get_grid(f)

    assert path_product(grid) == 336
