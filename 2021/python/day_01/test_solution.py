from .solution import parse, solve, window_sum


data = """199
200
208
210
200
207
240
269
260
263"""


def test_solution():
    assert solve(parse(data)) == (7, 5)


def test_window_sum():
    assert list(window_sum(parse(data), 3)) == [
        607, 618, 618, 617, 647, 716, 769, 792
    ]
