from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


def parse(data):
    return [line.strip() for line in data.split("\n") if line.strip()]


def solve(input):
    tree, levels = build_tree(input)
    g1, e1 = compute_1(input)
    ogr, co2 = compute_2(input)
    return g1 * e1, ogr * co2


@dataclass
class Node:
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Optional[int] = None
    leaves: int = 0

    def update_leaves(self):
        if self.left is None and self.right is None:
            self.leaves = 1  # We are a leaf
        else:
            if self.left is not None:
                self.left.update_leaves()
                self.leaves += self.left.leaves
            if self.right is not None:
                self.right.update_leaves()
                self.leaves += self.right.leaves

    def left_leaves(self):
        if self.left is None:
            return 0
        return self.left.leaves

    def right_leaves(self):
        if self.right is None:
            return 0
        return self.right.leaves


def build_tree(input):
    root = Node()
    levels = defaultdict(list)

    for line in input:
        current = root
        for k, c in enumerate(line):
            if c == "0":
                if current.left:
                    current = current.left
                else:
                    current.left = Node(value="0")
                    current = current.left
                    levels[k].append(current)
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = Node(value="1")
                    current = current.right
                    levels[k].append(current)

    root.update_leaves()
    return root, levels


def tree_compute_1(levels):
    bits = []

    for k in range(len(levels)):
        zeros = sum(n.leaves for n in levels[k] if n.value == "0")
        ones = sum(n.leaves for n in levels[k] if n.value == "1")
        bits.append("1" if ones >= zeros else "0")

    gamma = int("".join(bits), 2)
    return gamma, (2 ** len(bits) - 1) ^ gamma


def tree_compute_2(tree_root):
    ogr_bits = []
    co2_bits = []
    current = tree_root

    while current.left or current.right:
        left_leaves, right_leaves = (
            current.left_leaves(), current.right_leaves()
        )
        if right_leaves >= left_leaves and current.right:
            current = current.right
        else:
            current = current.left

        ogr_bits.append(current.value)

    current = tree_root
    while current.left or current.right:
        left_leaves, right_leaves = (
            current.left_leaves(), current.right_leaves()
        )
        if (right_leaves < left_leaves and current.right) or not current.left:
            current = current.right
        else:
            current = current.left

        co2_bits.append(current.value)

    return int("".join(ogr_bits), 2), int("".join(co2_bits), 2)


# Below is the old solution - using lists. Above, we use trees.
def compute_1(input):
    gamma_bits = compute_gamma_bits(input)
    gamma = int(gamma_bits, 2)
    # Flip the bits by XORing
    epsilon = (2 ** len(gamma_bits) - 1) ^ gamma
    return gamma, epsilon


def compute_2(input):
    ogr_bits, co2_bits = search(input)
    return int(ogr_bits, 2), int(co2_bits, 2)


def compute_gamma_bits(input):
    bits = []
    for k in range(len(input[0])):
        ones = sum(1 for line in input if line[k] == "1")
        bits.append("1" if ones > len(input) // 2 else "0")
    return "".join(bits)


def search(input):
    # This is a tree search, but we're doing it wrong - ain't got time for
    # implementing a tree - even if it is Christmas!
    ogr = input
    co2 = input

    for k in range(len(input[0])):
        ones = sum(1 for line in ogr if line[k] == "1")
        zeros = len(ogr) - ones
        common = "1" if ones >= zeros else "0"
        ogr = [line for line in ogr if line[k] == common]
        if len(ogr) == 1:
            break

    for k in range(len(input[0])):
        ones = sum(1 for line in co2 if line[k] == "1")
        zeros = len(co2) - ones
        common = "1" if ones >= zeros else "0"
        co2 = [line for line in co2 if line[k] != common]
        if len(co2) == 1:
            break

    assert len(ogr) == 1, ogr
    assert len(co2) == 1, co2
    return ogr[0], co2[0]
