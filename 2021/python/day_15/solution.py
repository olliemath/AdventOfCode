from heapq import heappop, heappush


def parse(input):
    return [
        [int(x) for x in line] for line in input.strip().split("\n")
    ]


def solve(input):
    return dijkstra(input, m=1), dijkstra(input, m=5)


def dijkstra(grid, m=1):
    q = [(0, 0, 0)]
    R0 = len(grid)
    C0 = len(grid[0])
    R = R0 * m
    C = C0 * m
    R_1 = R - 1
    C_1 = C - 1
    maxval = 9 * R * C
    d = {i: {j: maxval for j in range(C)} for i in range(R)}
    target = (R - 1, C - 1)

    while q:
        prev, r, c = heappop(q)

        val = grid[r % R0][c % C0] + r // R0 + c // C0
        if val > 9:
            val = 1 + ((val - 1) % 9)

        if prev + val < d[r][c]:
            dist = d[r][c] = prev + val

            if r == R_1 and c == C_1:
                break

            if r >= 1:
                heappush(q, (dist, r-1, c))
            if r < R_1:
                heappush(q, (dist, r+1, c))
            if c >= 1:
                heappush(q, (dist, r, c-1))
            if c < C_1:
                heappush(q, (dist, r, c+1))

    return d[target[0]][target[1]] - d[0][0]
