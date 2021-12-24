import itertools
import json
import math
import re

NUM_REX = re.compile("[0-9]+")


def parse(input):
    return [line for line in input.strip().split("\n")]


def solve(input):
    return magnitude(compute(input)), compute2(input)


def compute(input):
    x = input[0]
    for y in input[1:]:
        x = add(x, y)
    return x


def compute2(input):
    best = 0
    for x, y in itertools.product(input, repeat=2):
        res = magnitude(add(x, y))
        if res > best:
            best = res
    return best


def add(x, y):
    new = f"[{x},{y}]"
    while True:
        explode_nodes = find_explode(new)
        if explode_nodes:
            new = do_explode(new, *explode_nodes)
            continue
        split_node = find_split(new)
        if split_node:
            new = do_split(new, *split_node)
            continue

        break

    return new


def traverse(sum):
    depth = 0
    current = []
    current_start = None
    for i, c in enumerate(sum):
        if c == "[":
            depth += 1
        elif c == ",":
            if current:
                yield int("".join(current)), depth, current_start, i
                current = []
                current_start = None
        elif c == "]":
            if current:
                yield int("".join(current)), depth, current_start, i
                current = []
                current_start = None
            depth -= 1
        else:
            current.append(c)
            if current_start is None:
                current_start = i


def find_split(tree):
    for num, _, start, stop in traverse(tree):
        if num >= 10:
            return num, start, stop


def do_split(tree, num, start, stop):
    lhs = tree[:start]
    rhs = tree[stop:]

    new_pair = "[{},{}]".format(
        math.floor(num / 2), math.ceil(num / 2)
    )

    return lhs + new_pair + rhs


def find_explode(tree):
    prev = (None, -1, None, None)
    for node in traverse(tree):
        if node[1] >= 5 and prev and prev[1] == node[1]:
            return prev, node
        else:
            prev = node


def do_explode(tree, lh, rh):
    chunks = []

    # LHS
    num, _, start, _ = lh
    lhs = tree[:start-1]  # -1 due to bracket

    matches = list(NUM_REX.finditer(lhs))
    if matches:
        match = matches[-1]
        num += int(match.group())
        chunks.append(lhs[:match.start()])
        chunks.append(str(num))
        chunks.append(lhs[match.end():])
    else:
        chunks.append(lhs)

    chunks.append("0")

    # RHS
    num, _, _, stop = rh
    rhs = tree[stop+1:]  # +1 due to bracket

    match = NUM_REX.search(rhs)
    if match:
        num += int(match.group())
        chunks.append(rhs[:match.start()])
        chunks.append(str(num))
        chunks.append(rhs[match.end():])
    else:
        chunks.append(rhs)

    return "".join(chunks)


def explode(tree):
    node = find_explode(tree)
    if node:
        return do_explode(tree, *node)


def magnitude(tree):
    if isinstance(tree, str):
        return magnitude(json.loads(tree))
    if isinstance(tree, int):
        return tree
    return 3 * magnitude(tree[0]) + 2 * magnitude(tree[1])
