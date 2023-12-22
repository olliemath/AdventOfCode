from __future__ import annotations

from collections import defaultdict, deque
from operator import ge, gt, le, lt


def parse(data):
    instructions, parts = data.strip().split("\n\n")

    parsed_parts = []
    parts = parts.split("\n")
    for part in parts:
        parsed = {}
        for chunk in part[1:-1].split(","):
            name, value = chunk.split("=")
            parsed[name] = int(value)
        parsed_parts.append(parsed)

    parsed_instructions = {}
    for ins in instructions.split("\n"):
        name, value = ins[:-1].split("{")
        parsed_instructions[name] = parse_ins(value)

    return parsed_instructions, parsed_parts


def parse_ins(ins):
    if ":" not in ins:
        return ins

    test, lr = ins.split(":", 1)
    left, right = lr.split(",", 1)
    if ":" in left:
        left = parse_ins(left)
    if ":" in right:
        right = parse_ins(right)

    if ">" in test:
        name, value = test.split(">")
        value = int(value)
        test = (name, gt, value)
    elif "<" in test:
        name, value = test.split("<")
        value = int(value)
        test = (name, lt, value)

    return (test, left, right)


def solve(input):
    return part1(input), part2(input)


def part1(input):
    instructions, parts = input
    total = 0
    for part in parts:
        if run(instructions, part) == "A":
            total += sum(part.values())
    return total


def run(instructions, part):
    ins = instructions["in"]

    while ins not in ("R", "A"):
        if isinstance(ins, tuple):
            test, left, right = ins
            key, op, value = test
            if op(part[key], value):
                ins = left
            else:
                ins = right
        else:
            ins = instructions[ins]

    return ins


def part2(input):
    instructions, _ = input

    # fist treat it as a graph and find all paths to A
    graph = defaultdict(dict)
    rev_graph = defaultdict(dict)
    for name, ins in instructions.items():
        build_graph(name, ins, graph, rev_graph)

    # assume no cycles?
    paths = []

    queue = deque([(["A"], {k: (1, 4000) for k in "xmas"})])
    while queue:
        path, here_bounds = queue.popleft()
        here = path[-1]
        if here in rev_graph:
            for prev, prev_test in rev_graph[here].items():
                prev_key, prev_op, prev_val = prev_test
                bounds = here_bounds[prev_key]
                if prev_op == gt:
                    new_bounds = (max(prev_val + 1, bounds[0]), bounds[1])
                elif prev_op == ge:
                    new_bounds = (max(prev_val, bounds[0]), bounds[1])
                elif prev_op == lt:
                    new_bounds = (bounds[0], min(prev_val - 1, bounds[1]))
                elif prev_op == le:
                    new_bounds = (bounds[0], min(prev_val, bounds[1]))

                if new_bounds[0] > new_bounds[1]:
                    continue  # impossible

                new_path = path + [prev]
                if prev == "in":
                    paths.append((new_path, here_bounds | {prev_key: new_bounds}))
                else:
                    queue.append((new_path, here_bounds | {prev_key: new_bounds}))

    # there are quicker algos to get rid of the overlap, but let's just do this!
    total = 0

    for path in paths:
        hypercube = path[-1]
        size = 1
        for lower, upper in hypercube.values():
            size *= 1 + upper - lower
        total += size

    return total


def build_graph(name, ins, graph, rev_graph):
    if name in graph:
        return

    test, left, right = ins
    if isinstance(left, str):
        if isinstance(right, str) and left == right:
            graph[name][left] = (test[0], ge, 1)  # tautology
            rev_graph[left][name] = (test[0], ge, 1)  # tautology
            return

        graph[name][left] = test
        rev_graph[left][name] = test
    else:
        new_name = f"{name}-left"
        graph[name][new_name] = test
        rev_graph[new_name][name] = test

        build_graph(new_name, left, graph, rev_graph)

    tk, to, tv = test
    if to == gt:
        to = le
    else:
        to = ge

    not_test = (tk, to, tv)
    if isinstance(right, str):
        graph[name][right] = not_test
        rev_graph[right][name] = not_test
    else:
        new_name = f"{name}-right"
        graph[name][new_name] = not_test
        rev_graph[new_name][name] = not_test

        build_graph(new_name, right, graph, rev_graph)
