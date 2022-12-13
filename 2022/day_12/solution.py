import math
from heapq import heappush, heappop


def parse(data):
    grid = {}
    start, end = None, None
    for y, line in enumerate(data.strip().split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                c = "a"
            elif c == "E":
                end = (x, y)
                c = "z"

            grid[(x, y)] = ord(c) - ord("a")

    return grid, start, end


def solve(input):
    grid, start, end = input

    graph = {}
    for (x, y), height in grid.items():
        graph[(x, y)] = {}
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            v, w = x + dx, y + dy
            if (v, w) in grid:
                # We work backwards from the end, so are interested
                # in going downhill..
                delta = grid[(v, w)] - height
                if delta >= -1:
                    graph[(x, y)][(v, w)] = delta

    part1 = shortest_path(graph, end, [start])
    possible_starts = [v for v in grid if grid[v] == 0]
    part2 = shortest_path(graph, end, possible_starts)

    return part1, part2


def shortest_path(graph, start, ends):
    dists = {}
    queue = [(0, start)]

    while queue:
        dist, vertex = heappop(queue)
        if vertex not in dists or dist < dists[vertex]:
            dists[vertex] = dist
            if all(e in dists for e in ends):
                break

            for neighbour in graph[vertex]:
                heappush(queue, (dist + 1, neighbour))

    return min(dists.get(e, math.inf) for e in ends)
