import os

from day_03.solution import get_grid, path_count


FIXDIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "fixtures"
)


def test_path_count():

    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        grid = get_grid(f)

    assert path_count(grid) == 7
