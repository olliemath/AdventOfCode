from itertools import islice
from math import prod


hexmap = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

ops = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    4: lambda v: v,
    5: lambda v: int(v[0] > v[1]),
    6: lambda v: int(v[0] < v[1]),
    7: lambda v: int(v[0] == v[1]),
}


def parse(input):
    return "".join(hexmap[c] for c in input.strip())


def solve(input):
    result = parse_bytes(iter(input))
    return sum_versions(result), run_code(result)


def sum_versions(res):
    v, _, r = res

    if isinstance(r, list):
        v += sum(map(sum_versions, r))

    return v


def run_code(res):
    _, t, r = res

    if isinstance(r, list):
        r = list(map(run_code, r))

    return ops[t](r)


def parse_bytes(input):
    v_str = "".join(islice(input, 3))
    if not v_str:
        raise StopIteration

    v = int(v_str, 2)
    t = int("".join(islice(input, 3)), 2)

    if t == 4:
        packets = []
        should_break = False
        while not should_break:
            should_break = next(input) == "0"
            packets.append("".join(islice(input, 4)))

        return v, t, int("".join(packets), 2)

    elif next(input) == "0":
        length = int("".join(islice(input, 15)), 2)
        subinput = islice(input, length)

        subpackets = []
        while True:
            try:
                subpackets.append(parse_bytes(subinput))
            except StopIteration:
                break

        return v, t, subpackets

    else:
        length = int("".join(islice(input, 11)), 2)

        subpackets = []
        for _ in range(length):
            subpackets.append(parse_bytes(input))

        return v, t, subpackets
