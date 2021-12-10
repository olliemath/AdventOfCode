def parse(lines):
    for line in lines:
        places, letter, value = line.strip().split()
        places = [int(p) - 1 for p in places.split("-")]
        letter = letter[0]

        yield {
            "value": value,
            "policy": {
                "required": letter,
                "places": places,
            },
        }


def valid(password):
    letter = password["policy"]["required"]
    places = password["policy"]["places"]
    value = password["value"]

    count = sum(value[p] == letter for p in places)
    return count == 1


def num_valid(lines):
    return sum(1 for p in parse(lines) if valid(p))


def solve(input):
    print(num_valid(input), "valid")
