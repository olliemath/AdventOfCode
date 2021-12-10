from day_05.solution import parse, compute, solve


data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

grid_data = """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111...."""


diag_data = """1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111...."""


def test_parse():
    parsed = parse(data)
    assert parsed[0] == ((0, 9), (5, 9))


def test_compute_no_diag():
    grid = compute(parse(data))
    stringy_grid = ["." * 10] * 10
    for y, row in grid.items():
        for x, val in row.items():
            srow = stringy_grid[y]
            stringy_grid[y] = srow[:x] + str(val) + srow[x+1:]

    expected = grid_data.split("\n")

    for actual_row, expected_row in zip(stringy_grid, expected):
        assert actual_row == expected_row


def test_compute_diag():
    grid = compute(parse(data), diagonals=True)
    stringy_grid = ["." * 10] * 10
    for y, row in grid.items():
        for x, val in row.items():
            srow = stringy_grid[y]
            stringy_grid[y] = srow[:x] + str(val) + srow[x+1:]

    expected = diag_data.split("\n")

    for actual_row, expected_row in zip(stringy_grid, expected):
        assert actual_row == expected_row


def test_solve():
    assert solve(parse(data)) == (5, 12)
