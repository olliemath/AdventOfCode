from __future__ import annotations

from collections import defaultdict


def parse(data):
    return data.strip().split()


def solve(input):
    numbers = []
    gears = defaultdict(list)
    to_check = set()
    current = ""

    for i, line in enumerate(input):
        for j, char in enumerate(line):
            if char.isdigit():
                current += char
                for id in (-1, 0, 1):
                    for jd in (-1, 0, 1):
                        to_check.add((i + id, j + jd))

            elif current:
                partnumber = False

                for ic, jc in to_check:
                    if ic < 0 or ic >= len(input) or jc < 0 or jc >= len(input[0]):
                        continue

                    char = input[ic][jc]
                    if char != "." and not char.isdigit():
                        partnumber = True
                        if char == "*":
                            gears[(ic, jc)].append(int(current))

                if partnumber:
                    numbers.append(int(current))

                current = ""
                to_check = set()

        if current:
            partnumber = False

            for ic, jc in to_check:
                if ic < 0 or ic >= len(input) or jc < 0 or jc >= len(input[0]):
                    continue

                char = input[ic][jc]
                if char != "." and not char.isdigit():
                    partnumber = True
                    if char == "*":
                        gears[(ic, jc)].append(int(current))

            if partnumber:
                numbers.append(int(current))

            current = ""
            to_check = set()

    part1 = sum(numbers)

    # Find gears adjacent to 2 numbers
    part2 = sum(numbers[0] * numbers[1] for numbers in gears.values() if len(numbers) == 2)

    return part1, part2
