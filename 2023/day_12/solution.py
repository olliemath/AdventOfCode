from __future__ import annotations

from functools import lru_cache


def parse(data):
    rows = [row.split() for row in data.strip().split("\n")]
    return [(r[0], list(map(int, r[1].split(",")))) for r in rows]


def solve(input):
    return part1(input), part2(input)


def part1(input):
    total = 0
    for line, required in input:
        total += combos2(line, list(required))

    return total


def part2(input):
    total = 0

    for line, required in input:
        newline = "?".join(line for _ in range(5))
        total += combos2(newline, required * 5)

    return total


def combos(line, required):
    newreq = ["#" * r + "." for r in required]
    newreq[-1] = newreq[-1][:-1]
    return consuminate(list(line), newreq, len(line))


def consuminate(line, required, fin, seen=None):
    if seen is None:
        seen = {}
    elif (len(required), fin) in seen:
        return seen[(len(required), fin)]

    total = 0

    # try and place the final requirement at the end and recurse
    req = required.pop()
    for offset in range(fin - len(req), -1, -1):
        if match(line, req, offset):
            if not required:
                # there should now be no #s to our left
                for i, c in enumerate(line):
                    if i >= offset:
                        total += 1  # all .? to the left :)
                        break
                    elif c == "#":  # some # to the left :(
                        break
            else:
                seen[(len(required), offset)] = extra = consuminate(line, required, offset, seen)
                total += extra

        # check no # gets introduced to the right
        if line[offset + len(req) -1] == "#":
            break

    required.append(req)
    return total


def match(line, req, offset):
    for n, c in enumerate(req):
        if line[offset + n] not in (c, "?"):
            return False

    return True


# Faster implementation
def combos2(line, required):
    return consuminate2(line, tuple(required))


@lru_cache
def consuminate2(line, requiremets):

    if len(requiremets) == 0:
        return "#" not in line
    if sum(requiremets) + len(requiremets) - 1 > len(line):
        return 0  # line not long enough to fit all requirements

    if line[0] == ".":
        return consuminate2(line[1:], requiremets)

    total = 0
    if line[0] == "?":
        total += consuminate2(line[1:], requiremets)

    if "." not in line[:requiremets[0]] and (len(line) == requiremets[0] or len(line) > requiremets[0] and line[requiremets[0]] != "#"):
        total += consuminate2(line[requiremets[0] + 1:], requiremets[1:])

    return total
