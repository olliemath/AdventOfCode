from __future__ import annotations


def parse(data):
    return [list(map(int, line.split())) for line in data.strip().split("\n")]


def solve(input):
    extensions = [extend_history(line) for line in input]
    return sum(e[-1] for e in extensions), sum(e[0] for e in extensions)


def extend_history(nums):
    initial = [nums[0]]
    final = [nums[-1]]

    while not all(d == 0 for d in nums):
        nums = [b - a for a, b in zip(nums[:-1], nums[1:])]
        initial.append(nums[0])
        final.append(nums[-1])

    return sum(initial[::2]) - sum(initial[1::2]), sum(final)
