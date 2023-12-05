import pytest

from .solution import parse, best


data = "\n".join((
    "Blueprint 1:"
    "  Each ore robot costs 4 ore."
    "  Each clay robot costs 2 ore."
    "  Each obsidian robot costs 3 ore and 14 clay."
    "  Each geode robot costs 2 ore and 7 obsidian.",
    "Blueprint 2:"
    "  Each ore robot costs 2 ore."
    "  Each clay robot costs 3 ore."
    "  Each obsidian robot costs 3 ore and 8 clay."
    "  Each geode robot costs 3 ore and 12 obsidian.",
))


def test_parse():
    assert parse(
        "Blueprint 24: Each ore robot costs 2 ore. "
        "Each clay robot costs 3 ore. "
        "Each obsidian robot costs 2 ore and 16 clay. "
        "Each geode robot costs 2 ore and 9 obsidian."
    ) == [{
        "ore": {"ore": 2},
        "clay": {"ore": 3},
        "obsidian": {"ore": 2, "clay": 16},
        "geode": {"ore": 2, "obsidian": 9},
    }]


@pytest.mark.parametrize("i,expected", [(0, 9), (1, 12)])
def test_best(i, expected):
    parsed = parse(data)
    blueprint = parsed[i]
    assert best(blueprint=blueprint) == expected


@pytest.mark.parametrize("i,expected", [(0, 56), (1, 62)])
def test_best2(i, expected):
    parsed = parse(data)
    blueprint = parsed[i]
    assert best(blueprint=blueprint, N=32) == expected
