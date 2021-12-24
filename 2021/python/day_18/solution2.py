import itertools
import json
import math
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid1


def parse(input):
    return [json.loads(line) for line in input.strip().split("\n")]


def treeify(input):

    if isinstance(input, int):
        return SnailNum(value=input)

    return SnailNum(
        left=treeify(input[0]), right=treeify(input[1])
    )


def solve(input):
    return compute(input).magnitude(), compute2(input)


def compute(input):
    x = treeify(input[0])
    for y in input[1:]:
        x = add(x, treeify(y))
    return x


def compute2(input):
    best = 0
    for x, y in itertools.product(input, repeat=2):
        xt, yt = treeify(x), treeify(y)
        res = add(xt, yt).magnitude()
        if res > best:
            best = res

    return best


def add(x, y):
    new = SnailNum(left=x, right=y)

    while True:
        explode_node = find_explode(new)
        if explode_node:
            do_explode(explode_node)
            continue
        split_node = find_split(new)
        if split_node:
            do_split(split_node)
            continue

        break

    return new


def ordering(tree, level=0, out=None, seen=None):
    if tree.left:
        if tree.left.isnum():
            yield tree.left, level + 1
        else:
            yield from ordering(tree.left, level + 1, out, seen)

    yield tree, level

    if tree.right:
        if tree.right.isnum():
            yield tree.right, level + 1
        else:
            yield from ordering(tree.right, level + 1, out, seen)

    return out


def traverse_left(node):

    parent = node.parent
    while parent and node == parent.left:
        node, parent = parent, parent.parent

    if parent is None:
        return

    node = parent.left
    while True:
        if node.isnum():
            return node

        if node.right:
            if node.right.isnum():
                return node.right
            else:
                node = node.right


def traverse_right(node):

    parent = node.parent
    while parent and node == parent.right:
        node, parent = parent, parent.parent

    if parent is None:
        return

    node = parent.right
    while True:
        if node.isnum():
            return node

        if node.left:
            if node.left.isnum():
                return node.left
            else:
                node = node.left


def find_split(tree):
    for node, _ in ordering(tree):
        if node.isnum() and node.value >= 10:
            return node


def do_split(node):
    node.left = SnailNum(value=math.floor(node.value / 2), parent=node)
    node.right = SnailNum(value=math.ceil(node.value / 2), parent=node)
    node.value = None


def find_explode(tree):
    for node, level in ordering(tree):
        if (
            level >= 4
            and not node.isnum()
            and node.left.isnum()
            and node.right.isnum()
        ):
            return node


def do_explode(node):
    lnode = traverse_left(node)
    if lnode:
        lnode.value += node.left.value

    rnode = traverse_right(node)
    if rnode:
        rnode.value += node.right.value

    replacement = SnailNum(value=0)
    if node.parent:
        replacement.parent = node.parent
        if node.parent.left == node:
            node.parent.left = replacement
        elif node.parent.right == node:
            node.parent.right = replacement
        else:
            raise RuntimeError("Could not find node on parent")


def explode(tree):
    node = find_explode(tree)
    if node:
        do_explode(node)
        return tree


@dataclass
class SnailNum:

    value: Optional[int] = None
    left: Optional["SnailNum"] = None
    right: Optional["SnailNum"] = None
    parent: Optional["SnailNum"] = None
    _uuid: UUID = field(default_factory=uuid1)
    level: int = 0

    def __post_init__(self):
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def isnum(self):
        return self.value is not None

    def to_list(self):
        if self.isnum():
            return self.value

        return [self.left.to_list(), self.right.to_list()]

    def __eq__(self, other):
        return self._uuid == other._uuid

    def __repr__(self):
        return repr(self.to_list())

    def __str__(self):
        return str(self.to_list())

    def magnitude(self):
        if self.isnum():
            return self.value

        return self.left.magnitude() * 3 + self.right.magnitude() * 2
