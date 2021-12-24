from day_23.solution import solve, parse, target


def test_parse():
    p1, p2 = parse(data)
    assert p1 == (
        "AB",
        "DC",
        "CB",
        "AD",
        (),
    )

    assert p2 == (
        "ADDB",
        "DBCC",
        "CABB",
        "ACAD",
        (),
    )


def test_target():
    assert target(rs=2) == ("AA", "BB", "CC", "DD", ())
    assert target(rs=3) == ("AAA", "BBB", "CCC", "DDD", ())


def test_solve():
    assert solve(parse(data)) == (12521, 44169)


data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
