from __future__ import annotations

from .solution import parse, part1, part2, hash

data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def test_hash():
    assert hash("HASH") == 52


def test_solution():
    assert part1(parse(data)) == 1320
    assert part2(parse(data)) == 145
