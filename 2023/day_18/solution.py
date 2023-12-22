from __future__ import annotations

from collections import defaultdict

import tqdm


def parse(data):
    rows = []
    for row in data.strip().split("\n"):
        dir, dist, colour = row.split()
        dist = int(dist)
        colour = colour[2:-1]
        rows.append((dir, dist, colour))

    return rows


def solve(input):
    return part1(input), part2(input)


TRANSITIONS = {
    "U": lambda pair, delta=1: (pair[0] - delta, pair[1]),
    "D": lambda pair, delta=1: (pair[0] + delta, pair[1]),
    "L": lambda pair, delta=1: (pair[0], pair[1] - delta),
    "R": lambda pair, delta=1: (pair[0], pair[1] + delta),
}


def part1(input):
    directions = []
    for dir, dist, _ in input:
        directions.append((dir, dist))
    return count_interior(directions)


def part2(input):
    directions = []
    for _, _, colour in input:
        match colour[-1]:
            case "0":
                dir = "R"
            case "1":
                dir = "D"
            case "2":
                dir = "L"
            case "3":
                dir = "U"

        dist = int(colour[:-1], 16)
        directions.append((dir, dist))

    return count_interior(directions)


# TODO: shoelace algorithm
def count_interior(directions):
    maxi, mini = 0, 0
    maxj, minj = 0, 0
    current = (0, 0)
    occupado = defaultdict(dict)

    for dir, dist in tqdm.tqdm(directions):
        if dir in ("LR"):
            occupado[current[0]][current[1]] = dir
            current = TRANSITIONS[dir](current, dist)
            maxi = max(maxi, current[0] + 1)
            mini = min(mini, current[0])
            maxj = max(maxj, current[1] + 1)
            minj = min(minj, current[1])
        else:
            for _ in range(dist):
                occupado[current[0]][current[1]] = dir
                current = TRANSITIONS[dir](current)
                maxi = max(maxi, current[0] + 1)
                mini = min(mini, current[0])
                maxj = max(maxj, current[1] + 1)
                minj = min(minj, current[1])

    interior = 0
    for i in tqdm.tqdm(range(mini, maxi)):
        inside = False
        prev = ""
        row_occupado = sorted(occupado[i].items())
        interior += 1

        for (j, dir), (next_j, next_dir) in zip(row_occupado, row_occupado[1:]):
            interior += 1
            if dir == "U":
                if prev:
                    if prev == "U":
                        inside = not inside
                    prev = ""
                elif next_dir == "L":
                    # Fill up to this dude
                    interior += next_j - j - 1
                    prev = "U"
                else:
                    inside = not inside

            elif dir == "D":
                if prev:
                    if prev == "D":
                        inside = not inside
                    prev = ""
                elif next_dir == "L":
                    # Fill up to this dude
                    interior += next_j - j - 1
                    prev = "D"
                else:
                    inside = not inside

            elif dir == "R" and not prev:
                # Look immediately below/above
                if occupado.get(i + 1, {}).get(j, "") == "U":
                    prev = "U"  # F
                if occupado.get(i - 1, {}).get(j, "") == "D":
                    prev = "D"  # L

                # Fill up to next dude
                interior += next_j - j - 1

            elif prev:
                if occupado.get(i + 1, {}).get(j, "") == prev:
                    inside = not inside
                if occupado.get(i - 1, {}).get(j, "") == prev:
                    inside = not inside
                prev = ""

            if inside and dir != "R" and next_dir != "L":
                interior += next_j - j - 1

    return interior
