import itertools
import string

PRIORITIES = {a: i + 1 for i, a in enumerate(string.ascii_letters)}


def parse(data):
    return data.strip().split("\n")


def solve(input):
    return part1(input), part2(input)


def part1(input):
    result = 0
    for rucksack in input:
        first = set(rucksack[:len(rucksack) // 2])
        second = set(rucksack[len(rucksack) // 2:])
        char = next(iter(first.intersection(second)))
        result += PRIORITIES[char]

    return result


def part2(input):
    input = iter(input)
    result = 0

    while group := list(itertools.islice(input, 3)):
        badge = next(iter(set(group[0]).intersection(group[1], group[2])))
        result += PRIORITIES[badge]

    return result
