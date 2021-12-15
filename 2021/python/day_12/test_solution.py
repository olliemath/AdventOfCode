from day_12.solution import find_paths, parse, solve


data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

data2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

data3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def test_parse():
    parsed = parse(data)
    expected = {
        "start": {"A", "b"},
        "A": {"start", "b", "c", "end"},
        "b": {"start", "d", "A", "end"},
        "c": {"A"},
        "d": {"b"},
        "end": {"A", "b"},
    }

    assert parsed == expected


def test_find_paths():
    parsed = parse(data)
    expected = {
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "end"),
    }
    assert find_paths(parsed) == expected


def test_find_paths_data2():
    parsed = parse(data2)
    expected_str = """start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end"""
    expected = {
        tuple(line.split(",")) for line in expected_str.strip().split("\n")
    }
    assert find_paths(parsed) == expected


def test_solve():
    parsed = parse(data3)
    assert solve(parsed) == (226, 3509)
