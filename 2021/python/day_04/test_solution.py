from day_04.solution import compute, parse, play_bingo


data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def test_parse():
    draw, grids = parse(data)
    assert isinstance(draw, list)
    for d in draw:
        assert isinstance(d, int)

    assert isinstance(grids, list)
    assert len(grids) == 3


def test_play_bingo():
    draw, grids = parse(data)
    winning_order = play_bingo(draw, grids)
    winning_number, winning_grid = winning_order[0]
    assert winning_number == 24
    assert winning_grid == 188

    loosing_number, loosing_grid = winning_order[-1]
    assert loosing_number == 13
    assert loosing_grid == 148


def test_compute():
    draw, grids = parse(data)
    assert compute(draw, grids) == (4512, 1924)
