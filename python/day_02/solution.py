def parse(lines):
    for line in lines:
        bounds, letter, value = line.strip().split()
        min_, max_ = map(int, bounds.split("-"))
        letter = letter[0]

        yield {
            "value": value,
            "policy": {
                "required": letter,
                "min": min_,
                "max": max_,
            },
        }


def valid(password):
    letter = password["policy"]["required"]
    min_ = password["policy"]["min"]
    max_ = password["policy"]["max"]
    count = sum(1 for c in password["value"] if c == letter)

    return min_ <= count <= max_


def num_valid(lines):
    return sum(1 for p in parse(lines) if valid(p))


def solve(input):
    print(num_valid(input), "valid")
