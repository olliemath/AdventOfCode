REPLACEMENTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
REV_REPLACEMENTS = {"".join(reversed(k)): v for k, v in REPLACEMENTS.items()}


def parse(data):
    return data.strip().split()


def solve(input: list[str]):
    values1 = []
    values2 = []

    for row in input:
        # part 1
        first = find_first(row)
        last = find_first(reversed(row))
        if first and last:
            values1.append(int(first + last))

        # part 2
        first = find_first(row, replacements=REPLACEMENTS)
        last = find_first(reversed(row), replacements=REV_REPLACEMENTS)
        if first and last:
            values2.append(int(first + last))

    return sum(values1), sum(values2)


def find_first(row, replacements=None):
    subs = ""

    for char in row:
        if char.isdigit():
            return char
        elif replacements:
            subs += char
            for key, value in replacements.items():
                if subs.endswith(key):
                    return value
