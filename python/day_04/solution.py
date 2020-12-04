import functools

HEX = set("0123456789abcdef")
EYE_COLOURS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def validate_year(y, start, end):
    return len(y) == 4 and y.isnumeric() and start <= int(y) <= end


def validate_height(h):
    num, unit = h[:-2], h[-2:]
    if unit == "cm":
        return num.isnumeric() and 150 <= int(num) <= 193
    elif unit == "in":
        return num.isnumeric() and 59 <= int(num) <= 76


def validate_colour(c):
    return len(c) == 7 and c[0] == "#" and all(b in HEX for b in c[1:])


VALIDATORS = {
    "byr": functools.partial(validate_year, start=1920, end=2002),
    "iyr": functools.partial(validate_year, start=2010, end=2020),
    "eyr": functools.partial(validate_year, start=2020, end=2030),
    "hgt": validate_height,
    "hcl": validate_colour,
    "ecl": lambda c: c in EYE_COLOURS,
    "pid": lambda p: len(p) == 9 and p.isnumeric(),
}


def parse_batch(batch):
    passport = {}
    for line in batch:
        if not line.strip() and passport:
            yield passport
            passport = {}
        else:
            passport.update(f.split(":") for f in line.strip().split())

    # Pottential final passport in the file
    if passport:
        yield passport


def valid(passports):
    for p in passports:
        if all(
            field in p and validator(p[field])
            for field, validator in VALIDATORS.items()
        ):
            yield p


def get_num_valid(batch):
    return sum(1 for _ in valid(parse_batch(batch)))


def solve(input):
    print(get_num_valid(input), "valid")
