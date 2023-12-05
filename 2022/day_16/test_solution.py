from .solution import (
    parse, find_best_2xpath, find_best_path, build_shortest_paths
)


data = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def test_shortest_paths():
    shortest = build_shortest_paths(parse(data))

    assert shortest["AA"] == {
        "BB": 1,
        "DD": 1,
        "II": 1,
        "CC": 2,
        "EE": 2,
        "JJ": 2,
        "FF": 3,
        "GG": 4,
        "HH": 5,
    }
    assert shortest["BB"] == {
        "AA": 1,
        "CC": 1,
        "DD": 2,
        "II": 2,
        "EE": 3,
        "JJ": 3,
        "FF": 4,
        "GG": 5,
        "HH": 6,
    }


def test_find_best_path():
    input = parse(data)
    values = {k: v[0] for k, v in input.items() if v[0] > 0 and k != "AA"}
    shortest_paths = build_shortest_paths(input)

    best_path, best_score = find_best_path(
        values, shortest_paths, ["AA"], 3
    )
    assert best_path == ["AA", "DD"]
    assert best_score == 20

    best_path, best_score = find_best_path(
        values, shortest_paths, ["AA"], 5
    )
    assert best_path == ["AA", "DD", "EE"]
    assert best_score == 20 * 3 + 3

    best_path, best_score = find_best_path(
        values, shortest_paths, ["AA"], 7
    )
    assert best_path == ["AA", "DD", "BB"]
    assert best_score == 20 * 5 + 13 * 2

    expected = ["AA", "DD", "BB", "JJ", "HH", "EE", "CC"]
    best_path, best_score = find_best_path(
        values, shortest_paths, ["AA"], 30
    )
    assert best_path == expected
    assert best_score == 1651


def test_find_best_2xpath():
    input = parse(data)
    values = {k: v[0] for k, v in input.items() if v[0] > 0 and k != "AA"}
    shortest_paths = build_shortest_paths(input)

    best_path, best_score = find_best_2xpath(
        values, shortest_paths, [["AA"], ["AA"]], (26, 26)
    )
    assert best_score == 1707
