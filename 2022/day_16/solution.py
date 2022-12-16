import re
import heapq


def parse(data):
    rex = re.compile(r"^Valve ([A-Z]+) has flow rate=(\d+);[a-z ]+([A-Z, ]+)$")

    nodes = {}
    for row in data.strip().split("\n"):
        pieces = rex.match(row).groups()
        nodes[pieces[0]] = (int(pieces[1]), pieces[2].strip().split(", "))

    return nodes


def solve(input):
    # First we determine the distances between all of the nodes
    values = {k: v[0] for k, v in input.items() if v[0] > 0 and k != "AA"}
    shortest_paths = build_shortest_paths(input)
    return part1(values, shortest_paths), part2(values, shortest_paths)


def part1(values, shortest_paths):
    return find_best_path(values, shortest_paths, ["AA"], 0, 30)[1]


def part2(values, shortest_paths):
    return find_best_2xpath(
        values, shortest_paths, [["AA"], ["AA"]], 0, (26, 26)
    )[1]


def build_shortest_paths(input):
    paths = {}

    todo = list(reversed(input))
    while todo:
        start = todo.pop()
        dists = {start: 0}
        queue = [(0, start)]
        while queue:
            dist, node = heapq.heappop(queue)
            for neighbour in input[node][1]:
                if neighbour not in dists or dists[neighbour] > dist + 1:
                    dists[neighbour] = dist + 1
                    heapq.heappush(queue, (dist + 1, neighbour))

        # Now we've found the shortest paths!
        paths[start] = {k: v for k, v in dists.items() if k != start}

    return paths


def find_best_path(values, shortest_paths, current_path, current_score, time):
    if time <= 0 or len(values) == 0:
        return current_path, current_score

    best_path, best_score = current_path, current_score

    for k in list(values):
        new_time = time - shortest_paths[current_path[-1]][k] - 1
        if new_time <= 0:
            continue

        v = values.pop(k)
        current_path.append(k)
        new_path, new_score = find_best_path(
            values,
            shortest_paths,
            current_path,
            current_score + new_time * v,
            new_time,
        )
        if new_score >= best_score:
            best_path, best_score = new_path[:], new_score

        current_path.pop()
        values[k] = v

    return best_path, best_score


def find_best_2xpath(
    values, shortest_paths, current_paths, current_score, times
):
    if len(values) == 0 or times[0] <= 0 and times[1] <= 0:
        return current_paths, current_score

    best_paths, best_score = current_paths[:], current_score

    # We could do nothing and let the elephant take over, or vice versa!
    for k, (current_path, time) in enumerate(zip(current_paths, times)):
        new_path, new_score = find_best_path(
            values, shortest_paths, current_path, current_score, time
        )
        if new_score >= best_score:
            best_paths[k] = new_path
            best_score = new_score

    # Or we could cooperate (if there's enough moves left!)
    if len(values) > 1 and times[0] > 2 and times[1] > 2:
        for i, j in enumerate(list(values)):
            if current_paths == [["AA"], ["AA"]]:
                # Assume we start with lowest move
                elephant_moves = [k for k in list(values)[i + 1:]]
            else:
                elephant_moves = list(values)

            for k in elephant_moves:
                if j == k:
                    continue  # Can't both visit the same place next

                new_times = (
                    times[0] - shortest_paths[current_paths[0][-1]][j] - 1,
                    times[1] - shortest_paths[current_paths[1][-1]][k] - 1,
                )
                if new_times[0] <= 0 or new_times[1] <= 0:
                    continue

                vj, vk = values.pop(j), values.pop(k)
                current_paths[0].append(j)
                current_paths[1].append(k)
                new_paths, new_score = find_best_2xpath(
                    values,
                    shortest_paths,
                    current_paths,
                    current_score + new_times[0] * vj + new_times[1] * vk,
                    new_times,
                )

                if new_score >= best_score:
                    best_paths = [new_paths[0][:], new_paths[1][:]]
                    best_score = new_score

                current_paths[0].pop()
                current_paths[1].pop()
                values[j], values[k] = vj, vk

    return best_paths, best_score
