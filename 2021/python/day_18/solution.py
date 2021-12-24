import itertools
import json
import math
import re

NUM_REX = re.compile("[0-9]+")


def parse(input):
    lines = [line for line in input.strip().split("\n")]
    results = []
    for line in lines:
        result = []
        current = []
        for c in line:
            if c.isdecimal():
                current.append(c)
            elif current:
                result.append(int("".join(current)))
                if c != ",":
                    result.append(c)
                current = []
            elif c != ",":
                result.append(c)

        results.append(result)

    return results


def solve(input):
    return magnitude(compute(input)), compute2(input)


def compute(input):
    x = input[0]
    for y in input[1:]:
        x = add(x, y)

    return json.loads(smush(x))


def compute2(input):
    best = 0
    for x, y in itertools.product(input, repeat=2):
        res = magnitude(json.loads(smush(add(x, y))))
        if res > best:
            best = res
    return best


def add(x, y):
    new = ["["] + x + y + ["]"]
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


def find_split(tree):
    for i, c in enumerate(tree):
        if isinstance(c, int) and c >= 10:
            return i, c


def do_split(tree, idx, num):
    return tree[:idx] + [
        "[",  math.floor(num / 2), math.ceil(num / 2), "]"
    ] + tree[idx+1:]


def find_explode(tree):
    depth = 0
    prev = None
    prev_depth = None
    for i, c in enumerate(tree):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        else:
            if depth >= 5 and prev_depth == depth:
                return i, prev, c
            else:
                prev = c
                prev_depth = depth


def do_explode(tree, idx, lh, rh):
    # LHS
    lhs = tree[:idx-2]
    for i, c in enumerate(reversed(lhs)):
        if isinstance(c, int):
            lhs[len(lhs) - 1 - i] += lh
            break

    # RHS
    rhs = tree[idx+2:]
    for i, c in enumerate(rhs):
        if isinstance(c, int):
            rhs[i] += rh
            break

    lhs.append(0)
    lhs.extend(rhs)
    return lhs


def explode(tree):
    node = find_explode(tree)
    if node:
        return do_explode(tree, *node)


def magnitude(tree):
    if isinstance(tree, int):
        return tree
    return 3 * magnitude(tree[0]) + 2 * magnitude(tree[1])


def smush(tree):
    need_comma = False
    res = []
    for c in tree:
        if isinstance(c, int):
            if need_comma:
                res.append(",")
            else:
                need_comma = True
        elif c == "]":
            need_comma = True
        elif c == "[":
            if need_comma:
                res.append(",")
            need_comma = False

        res.append(str(c))

    res = "".join(res)
    return res
