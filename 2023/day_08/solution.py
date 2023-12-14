from __future__ import annotations

import itertools
import math


def parse(data):
    dirs, rawgraph = data.strip().split("\n\n")
    dirs = [0 if d == "L" else 1 for d in dirs]
    graph = {}

    for row in rawgraph.split("\n"):
        node, edges = row.split(" = ")
        left, right = edges[1:-1].split(", ")
        graph[node] = (left, right)

    return dirs, graph


def solve(input):
    return part1(input), part2(input)


def part1(input):
    return cycle_length(input, "AAA", "ZZZ")


def part2(input):
    return cycle_length(input, "A", "Z")


def cycle_length(input, start, stop):
    dirs, graph = input

    starts = [n for n in graph if n.endswith(start)]
    cycle_lengths = []
    for node in starts:
        for k, d in enumerate(itertools.cycle(dirs)):
            node = graph[node][d]
            if node.endswith(stop):
                cycle_lengths.append(k + 1)
                break


    return math.lcm(*cycle_lengths)
