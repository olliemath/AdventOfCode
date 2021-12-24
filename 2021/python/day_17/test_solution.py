from day_17.solution import (
    solve, find_paths, find_x_inter, find_y_inter, parse
)


data = "target area: x=20..30, y=-10..-5"


def test_parse():
    assert parse(data) == (20, 30, -10, -5)


def test_compute():
    box = parse(data)
    assert solve(box) == (45, 112)


def test_x_y_inter():
    box = parse(data)

    assert find_x_inter(box) == {
        6: (5, float("inf")),
        7: (4, float("inf")),
        8: (3, 5),
        9: (3, 4),
        10: (3, 3),
        11: (2, 3),
        12: (2, 2),
        13: (2, 2),
        14: (2, 2),
        15: (2, 2),
        20: (1, 1),
        21: (1, 1),
        22: (1, 1),
        23: (1, 1),
        24: (1, 1),
        25: (1, 1),
        26: (1, 1),
        27: (1, 1),
        28: (1, 1),
        29: (1, 1),
        30: (1, 1),
    }

    assert find_y_inter(box) == {
        -10: (1, 1),
        -9: (1, 1),
        -8: (1, 1),
        -7: (1, 1),
        -6: (1, 1),
        -5: (1, 1),
        -4: (2, 2),
        -3: (2, 2),
        -2: (2, 3),
        -1: (3, 4),
        0: (4, 5),
        1: (5, 6),
        2: (7, 7),
        3: (9, 9),
        4: (10, 10),
        5: (12, 12),
        6: (14, 14),
        7: (16, 16),
        8: (18, 18),
        9: (20, 20),
    }


def test_find_paths():
    box = parse(data)
    paths = find_paths(box)

    assert paths

    for path in paths:
        _, hits = compute_path(box, *path)
        assert hits

    assert (7, 2) in paths
    assert (6, 3) in paths
    assert (9, 0) in paths


def compute_path(box, vx, vy):
    hits = False
    path = []
    x, y = 0, 0
    while y >= box[-2]:

        x += vx
        y += vy

        vx = max(vx - 1, 0)
        vy -= 1

        path.append((x, y))

        if box[0] <= x <= box[1] and box[2] <= y <= box[3]:
            hits = True

    return path, hits
