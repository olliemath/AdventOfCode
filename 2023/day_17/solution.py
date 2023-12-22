from __future__ import annotations

import heapq
from collections import defaultdict


def parse(data):
    return [list(map(int, row)) for row in data.strip().split("\n")]


def solve(input):
    return part1(input), part2(input)


def part1(input):
    return lazy_shortest_path(input, 1, 3)


def part2(input):
    return lazy_shortest_path(input, minlen=4, maxlen=10)


def lazy_shortest_path(input, minlen=1, maxlen=3):
    # The shortest path to a square s for which there is no
    # legal next ">" move might not be the globally shortest,
    # but we don't know that within dijkstra. To preserve
    # other possibilities the idea is to keep both a square
    # and the direction we reach it from as separate nodes (s, >)
    # in a meta-graph

    # Leaving each of these vertexes we use only edges which
    # have a different direction from the way we arrived and
    # move us at least minlen and at most maxlen squares.
    # So a path looks e.g. like hop 3 squares >>> to (0, 3, >),
    # then hop 1 squrare v to (1, 3, v),
    # then hop 2 squares >> to (1, 5, >) etc etc.

    # The rest is just details and trying not to run out of memory

    dists = defaultdict(lambda: float("inf"))
    dists[(0, 0, "")] = 0
    queue = [(0, (0, 0, ""))]
    final_dists = {
        (len(input) - 1, len(input[0]) - 1, "v"): float("inf"),
        (len(input) - 1, len(input[0]) - 1, ">"): float("inf"),
    }

    prev = {}
    while queue:
        dist, node = heapq.heappop(queue)
        i, j, dir = node
        # now check adjacent nodes
        for runlen in range(minlen, maxlen + 1):
            if not dir:
                candidates = (
                    (i + runlen, j, "v"),
                    (i - runlen, j, "^"),
                    (i, j + runlen, ">"),
                    (i, j - runlen, "<"),
                )
            elif dir == "v":
                candidates = (
                    ((i, j + runlen, ">")),
                    ((i, j - runlen, "<")),
                )
            elif dir == "^":
                candidates = (
                    ((i, j + runlen, ">")),
                    ((i, j - runlen, "<")),
                )
            elif dir == ">":
                candidates = (
                    ((i + runlen, j, "v")),
                    ((i - runlen, j, "^")),
                )
            elif dir == "<":
                candidates = (
                    ((i + runlen, j, "v")),
                    ((i - runlen, j, "^")),
                )

            for other in candidates:
                if not (0 <= other[0] < len(input) and 0 <= other[1] < len(input[0])):
                    continue

                if other[-1] == "v":
                    newdist = dist + sum(
                        input[other[0] - n][other[1]] for n in range(runlen)
                    )
                elif other[-1] == "^":
                    newdist = dist + sum(
                        input[other[0] + n][other[1]] for n in range(runlen)
                    )
                elif other[-1] == ">":
                    newdist = dist + sum(
                        input[other[0]][other[1] - n] for n in range(runlen)
                    )
                elif other[-1] == "<":
                    newdist = dist + sum(
                        input[other[0]][other[1] + n] for n in range(runlen)
                    )

                if newdist < dists[other]:
                    dists[other] = newdist
                    prev[other] = node
                    heapq.heappush(queue, (newdist, other))

                    if other in final_dists:
                        final_dists[other] = newdist
                        if all(v < float("inf") for v in final_dists.values()):
                            best, best_dist = min(
                                final_dists.items(), key=lambda pair: pair[1]
                            )
                            return best_dist


def printpath(prev, node, input):
    path = {}
    while node != (0, 0, ""):
        path[(node[0], node[1])] = node[2][-1]
        node = prev[node]

    print()
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if (i, j) in path:
                char = path[(i, j)]
            print(char, end="")
        print()
