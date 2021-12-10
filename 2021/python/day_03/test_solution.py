from .solution import (
    build_tree,
    compute_1,
    compute_2,
    compute_gamma_bits,
    parse,
    search,
    tree_compute_1,
    tree_compute_2,
)


data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def test_compute_1():
    assert compute_gamma_bits(parse(data)) == "10110"
    assert compute_1(parse(data)) == (22, 9)


def test_search():
    assert search(parse(data)) == ("10111", "01010")
    assert compute_2(parse(data)) == (23, 10)


def test_tree_compute_1():
    _root, levels = build_tree(parse(data))
    assert tree_compute_1(levels) == (22, 9)


def test_tree_compute_2():
    root, _levels = build_tree(parse(data))
    assert tree_compute_2(root) == (23, 10)
