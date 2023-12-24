from __future__ import annotations

from .solution import parse, solve

data = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

data2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def test_solution():
    assert solve(parse(data), watch_low=()) == (32000000, 1)
    assert solve(parse(data2), watch_low=()) == (11687500, 1)
