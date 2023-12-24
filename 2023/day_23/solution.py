from __future__ import annotations


def parse(data):
    return data.strip().split("\n")


def solve(input):
    return part1(input), part2(input)


def part1(input, slippy=True):
    for i, char in enumerate(input[0]):
        if char == ".":
            start = (0, i)
    for i, char in enumerate(input[-1]):
        if char == ".":
            end = (len(input) - 1, i)

    complete_paths = set()
    to_process = [([start], {start})]

    while to_process:
        part_path = to_process.pop()
        i, j = part_path[0][-1]

        while True:
            candidates = []
            for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if ii < 0 or jj < 0 or ii >= len(input) or jj >= len(input[0]):
                    continue
                elif input[ii][jj] == "#":
                    continue
                elif (ii, jj) in part_path[1]:
                    continue
                elif slippy:
                    if ii > i and (input[i][j] == "^" or input[ii][j] == "^"):
                        continue
                    elif ii < i and (input[i][j] == "v" or input[ii][j] == "v"):
                        continue
                    elif jj > j and (input[i][j] == "<" or input[ii][j] == "<"):
                        continue
                    elif jj < j and (input[i][j] == ">" or input[ii][j] == ">"):
                        continue

                candidates.append((ii, jj))

            if not candidates:
                break
            elif len(candidates) == 1:
                i, j = candidates[0]
                part_path[0].append((i, j))
                part_path[1].add((i, j))
                if part_path[0][-1] == end:
                    complete_paths.add(len(part_path[0]))
                    break
                # for ii, row in enumerate(input):
                #     print()
                #     for jj, char in enumerate(row):
                #         if (ii, jj) in part_path[1]:
                #             print("O", end="")
                #         else:
                #             print(char, end="")
                # print()
            else:
                for ii, jj in candidates:
                    new_part_path = (
                        part_path[0] + [(ii, jj)],
                        part_path[1].union({(ii, jj)}),
                    )
                    if new_part_path[0][-1] == end:
                        complete_paths.add(len(new_part_path[0]))
                    else:
                        to_process.append(new_part_path)
                    # for ii, row in enumerate(input):
                    #     print()
                    #     for jj, char in enumerate(row):
                    #         if (ii, jj) in new_part_path[1]:
                    #             print("O", end="")
                    #         else:
                    #             print(char, end="")
                    # print()
                break

    return max(complete_paths) - 1


def part2(input):
    for i, char in enumerate(input[0]):
        if char == ".":
            start = (0, i)
    for i, char in enumerate(input[-1]):
        if char == ".":
            end = (len(input) - 1, i)

    from collections import defaultdict

    graph = defaultdict(dict)
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if char == "#":
                continue
            for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if ii < 0 or jj < 0 or ii >= len(input) or jj >= len(input[0]):
                    continue
                elif input[ii][jj] == "#":
                    continue
                else:
                    graph[(i, j)][(ii, jj)] = 1

    # now simplify the graph
    mutated = set(graph)
    while mutated:
        mutated = set()

        for node, neighbours in list(graph.items()):
            if len(neighbours) == 2 and node not in (start, end):
                neighbours = list(neighbours)
                n0_dist = graph[neighbours[0]].pop(node)
                n1_dist = graph[neighbours[1]].pop(node)
                graph[neighbours[0]][neighbours[1]] = n0_dist + n1_dist
                graph[neighbours[1]][neighbours[0]] = n0_dist + n1_dist
                mutated.update(neighbours)
                del graph[node]

    complete_paths = set()
    to_process = [([start], {start})]

    while to_process:
        part_path, part_path_set = to_process.pop()
        while True:
            good_candidates = [
                c for c in graph[part_path[-1]] if c not in part_path_set
            ]
            if len(good_candidates) == 0:
                break
            elif len(good_candidates) == 1:
                part_path.append(good_candidates[0])
                part_path_set.add(good_candidates[0])
                if good_candidates[0] == end:
                    complete_paths.add(
                        sum(graph[x][y] for x, y in zip(part_path[:-1], part_path[1:]))
                    )
                    break
            else:
                for c in good_candidates:
                    new_part_path = part_path + [c]
                    new_part_path_set = part_path_set.union([c])
                    if c == end:
                        complete_paths.add(
                            sum(
                                graph[x][y]
                                for x, y in zip(new_part_path[:-1], new_part_path[1:])
                            )
                        )
                    else:
                        to_process.append((new_part_path, new_part_path_set))

                break

    return max(complete_paths)
