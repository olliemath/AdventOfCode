from __future__ import annotations


def parse(data):
    return data.strip().split("\n")


def solve(input):
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if char == "S":
                component = get_component(input, i, j)
                break

    # Swap out S for its "True" character
    curve = list(component.values())
    enddir = curve[-1][1]
    startdir = {v: k for k, v in TRANSITIONS[curve[0][0]].items()}[curve[0][1]]
    for true_char, trans in TRANSITIONS.items():
        if (enddir, startdir) in trans.items():
            for i, row in enumerate(input):
                if "S" in row:
                    input[i] = row.replace("S", true_char)
                    break

    inside = compute_internals(input, component)
    return len(component) // 2, len(inside)


TRANSITIONS = {
    "-": {"l": "l", "r": "r"},
    "F": {"u": "r", "l": "d"},
    "|": {"u": "u", "d": "d"},
    "L": {"d": "r", "l": "u"},
    "J": {"r": "u", "d": "l"},
    "7": {"u": "l", "r": "d"},
}
DIRECTIONS = {
    "u": lambda x, y: (x - 1, y),
    "d": lambda x, y: (x + 1, y),
    "l": lambda x, y: (x, y - 1),
    "r": lambda x, y: (x, y + 1),
}


def get_component(input, i, j):
    # Look around for connecting items
    ext = []

    for d, f in DIRECTIONS.items():
        fi, fj = f(i, j)
        char = get(input, fi, fj)

        if char in TRANSITIONS and d in TRANSITIONS[char]:
            ext = extend(input, fi, fj, TRANSITIONS[char][d])
            if (i, j) in ext:
                return ext


def extend(input, i, j, d):

    char = get(input, i, j)
    result = {(i, j): (char, d)}
    while char != "S":
        i, j = DIRECTIONS[d](i, j)
        char = get(input, i, j)
        result[(i, j)] = (char, d)
        if char not in TRANSITIONS or d not in TRANSITIONS[char]:
            break

        d = TRANSITIONS[char][d]
        result[(i, j)] = (char, d)

    return result


def get(input, i, j):
    try:
        return input[i][j]
    except IndexError:
        return "."


def compute_internals(input, curve):
    internal = set()
    for i, row in enumerate(input):
        for j, _ in enumerate(row):
            if (i, j) in curve:
                continue
            else:
                # winding number algo
                winding = winding_number(i, j, input, curve)
                if winding != 0:
                    internal.add((i, j))

    return internal


def winding_number(i, j, input, curve):
    count = 0
    for fj in range(j + 1, len(input[0])):
        if (i, fj) in curve:
            char, d = curve[(i, fj)]

            if char == "|":
                count += 1 if d == "u" else -1
            elif char == "F":
                # Look ahead to get all stretches like F---J
                k = fj + 1
                while input[i][k] == "-":
                    k += 1
                other = input[i][k]
                if other == "J":  # FJ
                    count += (1 if d == "r" else -1)
            elif char == "L":
                # Look ahead to get all stretches like L---J
                k = fj + 1
                while input[i][k] == "-":
                    k += 1
                other = input[i][k]
                if other == "7":  # L7
                    count += (1 if d == "u" else -1)

    return count
