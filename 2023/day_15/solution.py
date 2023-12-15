from __future__ import annotations

from collections import defaultdict


def parse(data):
    return data.strip().split(",")


def solve(input):
    return part1(input), part2(input)


def part1(input):
    return sum(map(hash, input))


def part2(input):
    hashmap = defaultdict(dict)

    for item in input:
        if "=" in item:
            label, lens = item.split("=")
            key = hash(label)
            hashmap[key][label] = lens
        else:
            label = item[:-1]
            key = hash(label)
            hashmap[key].pop(label, None)

    total = 0
    for key, values in hashmap.items():
        for slot, lens in enumerate(values.values()):
            total += (key + 1) * (slot + 1) * int(lens)

    return total


def hash(string):
    result = 0
    for char in string:
        result = ((result + ord(char)) * 17) % 256
    return result
