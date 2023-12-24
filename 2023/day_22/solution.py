from __future__ import annotations

from collections import defaultdict


def parse(data):
    rows = data.strip().split("\n")
    result = []
    for row in rows:
        result.append(tuple(tuple(map(int, c.split(","))) for c in row.split("~")))

    return sorted(result, key=lambda r: min(r[0][-1], r[1][-1]))


def solve(input):
    settled = []

    for block in input:
        (x0, y0, z0), (x1, y1, z1) = block
        intersectors = [s for s in settled if inter(block, s)]
        lowest = max((max(z0, z1) for i in intersectors), default=0)

        block = (
            (x0, y0, lowest + 1 + z0 - min(z0, z1)),
            (x1, y1, lowest + 1 + z1 - min(z0, z1)),
        )
        settled.append(block)

    bottom_by_row = defaultdict(list)
    top_by_row = defaultdict(list)

    for s in settled:
        bottom_row = min(s[0][-1], s[1][-1])
        top_row = max(s[0][-1], s[1][-1])
        bottom_by_row[bottom_row].append(s)
        top_by_row[top_row].append(s)

    # build a graph connecting the blocks
    up_graph = defaultdict(list)
    dn_graph = defaultdict(list)
    for r, blocks in sorted(top_by_row.items()):
        above = bottom_by_row[r + 1]
        for b in blocks:
            if b not in up_graph:
                up_graph[b] = []
            for a in above:
                if inter(a, b):
                    up_graph[b].append(a)
                    dn_graph[a].append(b)

    # part1
    part1 = 0
    for above in up_graph.values():
        if not above or all(len(dn_graph[a]) > 1 for a in above):
            part1 += 1

    # part2
    part2 = 0
    for above in up_graph.values():
        will_fall = [a for a in above if len(dn_graph[a]) == 1]
        fallen = set(will_fall)

        while will_fall:
            candidates = set()
            for a in will_fall:
                candidates.update(up_graph[a])
            will_fall = [c for c in candidates if all(d in fallen for d in dn_graph[c])]
            fallen.update(will_fall)

        part2 += len(fallen)

    return part1, part2


def inter(a, b):
    ax0, ay0, _ = a[0]
    ax1, ay1, _ = a[1]

    bx0, by0, _ = b[0]
    bx1, by1, _ = b[1]

    return ax1 >= bx0 and ax0 <= bx1 and ay1 >= by0 and ay0 <= by1
