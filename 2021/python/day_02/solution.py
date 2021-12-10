def parse(data):
    lines = [d.strip() for d in data.split("\n") if d.strip()]
    pairs = [d.split() for d in lines]
    return [(p[0][0], int(p[1])) for p in pairs]


def solve(input):
    h1, d1 = do_instructions_1(input)
    h2, d2 = do_instructions_2(input)
    return h1 * d1, h2 * d2


def do_instructions_1(input):
    hor, depth = 0, 0
    for direction, amount in input:
        if direction == "f":
            hor += amount
        elif direction == "u":
            depth -= amount
        elif direction == "d":
            depth += amount

    return hor, depth


def do_instructions_2(input):
    aim, hor, depth = 0, 0, 0
    for direction, amount in input:
        if direction == "f":
            hor += amount
            depth += aim * amount
        elif direction == "u":
            aim -= amount
        elif direction == "d":
            aim += amount

    return hor, depth
