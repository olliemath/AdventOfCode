from day_13.solution import parse, fold_left, fold_up, compute


data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def test_fold_left():
    grid, folds = parse(data)
    assert len(grid) == 18

    grid = fold_up(grid, 7)
    assert len(grid) == 17

    grid = fold_left(grid, 5)
    assert len(grid) == 16
