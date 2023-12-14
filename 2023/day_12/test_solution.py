from __future__ import annotations

import pytest

from .solution import combos, parse, part2, solve

data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_combos():
    assert combos("???.###", [1, 1, 3]) == 1
    assert combos(".??..??...?##.", [1, 1, 3]) == 4
    assert combos("?###????????", [3, 2, 1]) == 10


@pytest.mark.parametrize(
    ["input", "expected"],
    (
        ([["???.###", [1, 1, 3]]], 1),
        ([[".??..??...?##.", [1, 1, 3]]], 16384),
        ([["?#?#?#?#?#?#?#?", [1, 3, 1, 6]]], 1),
        ([["????.#...#...", [4, 1, 1]]], 16),
        ([["????.######..#####.", [1, 6, 5]]], 2500),
        ([["?###????????", [3, 2, 1]]], 506250),
    ),
)
def test_part2(input, expected):
    assert part2(input) == expected


def test_solve():
    assert solve(parse(data)) == (21, 525152)
