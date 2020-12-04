import os

from day_02.solution import parse, valid


FIXDIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "fixtures"
)


def test_parse():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        passwords = list(parse(f))

    assert len(passwords) == 3
    assert passwords[0] == {
        "value": "abcde",
        "policy": {
            "required": "a",
            "places": [0, 2],
        },
    }


def test_valid():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        passwords = list(parse(f))

    assert valid(passwords[0])
    assert not valid(passwords[1])
    assert not valid(passwords[2])
