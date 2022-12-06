from .solution import parse, solve


data = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""


def test_part1():
    assert solve(parse(data))[0] == 7


def test_part2():
    for data, expected in (
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
    ):
        assert solve(data)[1] == expected
