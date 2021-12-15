from collections import defaultdict, deque


def parse(input):
    matrix = defaultdict(set)
    for line in input.strip().split("\n"):
        start, end = line.split("-")
        matrix[start].add(end)
        matrix[end].add(start)

    return matrix


def solve(input):
    return len(find_paths(input)), find_paths2(input)


def find_paths(matrix):
    paths = set()
    queue = deque()

    path = (["start"], set(["start"]))
    queue.append(path)

    while queue:
        path, visited = queue.popleft()
        to_visit = matrix[path[-1]]

        for cave in to_visit:
            if cave in visited:
                continue

            newpath = path + [cave]
            if cave == "end":
                paths.add(tuple(newpath))

            else:
                if cave.islower():
                    newvisited = visited.union({cave})
                else:
                    newvisited = visited

                queue.append((newpath, newvisited))

    return paths


def find_paths2(matrix, current=None, visited=None, twice_used=False):
    paths = 0

    if current is None:
        current = "start"
        visited = defaultdict(int)

    to_visit = matrix[current]
    for cave in to_visit:
        if cave == "start" or (twice_used and visited[cave]):
            continue

        if cave == "end":
            paths += 1
        else:
            if cave.islower():
                visited[cave] += 1
            paths += find_paths2(
                matrix,
                current=cave,
                visited=visited,
                twice_used=twice_used or visited[cave] > 1,
            )
            if cave.islower():
                visited[cave] -= 1

    return paths
