from day_09.solution import get_basins, get_basin, parse, compute1, compute2


data = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_parse():
    parsed = parse(data)
    assert len(parsed) == 5
    assert parsed[0] == "2199943210"


def test_compute1():
    assert compute1(parse(data)) == 15


def test_compute2():
    parsed = parse(data)
    basins = get_basins(parsed)
    assert sorted(basins) == [3, 9, 9, 14]
    assert compute2(parsed) == 1134


def test_get_basin():
    parsed = parse(data)
    assert get_basin(parsed, 0, 1, "1") == {(0, 0), (0, 1), (1, 0)}
