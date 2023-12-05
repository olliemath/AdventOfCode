from .solution import part1


data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_part1():
    grid = part1(data, N=1)
    assert grid == [0, 0, 1, 1, 1, 1, 0]
    grid = part1(data, N=2)
    assert grid == [0, 0, 3, 4, 3, 1, 0]
    grid = part1(data, N=3)
    assert grid == [4, 4, 6, 4, 3, 1, 0]
    grid = part1(data, N=4)
    assert grid == [4, 4, 6, 4, 7, 1, 0]
    grid = part1(data, N=5)
    assert grid == [4, 4, 6, 4, 9, 9, 0]
    grid = part1(data, N=6)
    assert grid == [4, 10, 10, 10, 10, 9, 0]
    grid = part1(data, N=7)
    assert grid == [4, 12, 13, 12, 10, 9, 0]
    grid = part1(data, N=8)
    assert grid == [4, 12, 13, 13, 13, 15, 0]
    grid = part1(data, N=9)
    assert grid == [4, 12, 13, 13, 17, 15, 0]
    grid = part1(data, N=10)
    assert grid == [14, 14, 13, 13, 17, 15, 0]

    grid = part1(data)
    assert max(grid) == 3068
