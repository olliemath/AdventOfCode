from __future__ import annotations

from .solution import parse, part1, part2

data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_solution():
    assert part1(parse(data)) == 19114
    assert part2(parse(data)) == 167409079868000


B = (
    ["A", "px-right", "px", "in"],
    ["A", "qs", "qqz", "in"],
    ["A", "qkq", "px", "in"],
    ["A", "lnx", "qs", "qqz", "in"],  # X2?
    ["A", "crn", "qkq", "px", "in"],
    ["A", "hdj", "qqz-right", "qqz", "in"],
    {"x": (1, 4000), "m": (839, 1800), "a": (1, 4000), "s": (1351, 2770)},
    ["A", "pv", "hdj", "qqz-right", "qqz", "in"],
    {"x": (1, 4000), "m": (1, 838), "a": (1, 1716), "s": (1351, 2770)},
    ["A", "rfg-right", "rfg", "px-right", "px", "in"],
    {"x": (1, 2440), "m": (1, 2090), "a": (2006, 4000), "s": (537, 1350)},
)
