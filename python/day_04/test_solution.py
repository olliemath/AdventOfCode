import os

from day_04.solution import parse_batch, get_num_valid, VALIDATORS


FIXDIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "fixtures"
)
VALIDATOR_TEST_CASES = [
    ("byr", True, "2002"),
    ("byr", False, "2003"),
    ("hgt", True, "60in"),
    ("hgt", True, "190cm"),
    ("hgt", False, "190in"),
    ("hgt", False, "190"),
    ("hcl", True, "#123abc"),
    ("hcl", False, "#123abz"),
    ("hcl", False, "123abc"),
    ("ecl", True, "brn"),
    ("ecl", False, "wat"),
    ("pid", True, "000000001"),
    ("pid", False, "0123456789"),
]


def test_parse_batch():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        parsed = list(parse_batch(f))

    assert len(parsed) == 4


def test_valid():
    with open(os.path.join(FIXDIR, "testfile.txt")) as f:
        valid_passports = get_num_valid(f)

    assert valid_passports == 2


def test_validators():

    for field, expected, value in VALIDATOR_TEST_CASES:
        validator = VALIDATORS[field]
        assert bool(validator(value)) == expected, \
            f"Expected {field}:{value} to give {expected}"


def test_invalid_passports():
    with open(os.path.join(FIXDIR, "invalid.txt")) as f:
        num_valid = get_num_valid(f)

    assert num_valid == 0


def test_valid_passports():
    with open(os.path.join(FIXDIR, "valid.txt")) as f:
        lines = list(f)

    num_valid = get_num_valid(lines)
    num_passports = sum(1 for _ in parse_batch(lines))

    assert num_valid == num_passports
