from heapq import heappop, heappush

ROOMS = dict(map(reversed, enumerate("ABCD")))
COSTS = {k: 10 ** v for k, v in ROOMS.items()}
ILLEGAL = {2, 4, 6, 8}


# Any configuration of dudes is a node
def target(rs):
    state = []
    for c in "ABCD":
        state.append(c * rs)
    state.append(())
    return tuple(state)


def solve(input):
    p1, p2 = input
    return dijkstra(p1, 2), dijkstra(p2, 4)


def dijkstra(dudes, rs=2):
    TARGET = target(rs)
    queue = [(0, dudes)]
    dists = {}

    while queue:
        dist, dudes = heappop(queue)

        if dudes not in dists or dist < dists[dudes]:
            dists[dudes] = dist
            if dudes == TARGET:
                return dist

            for new_dudes, cost in next_moves(dudes, rs):
                heappush(queue, (dist + cost, new_dudes))

    return None


def next_moves(dudes, rs=2):
    """Get next moves and their costs."""
    hall = dudes[-1]
    blocked = {t[0] for t in dudes[-1]}

    # First see if anyone can go to their room
    for p, d in hall:
        room = dudes[ROOMS[d]]
        roomlen = len(room)
        if not room or (roomlen < rs and all(other == d for other in room)):
            # If we're not blocked then let's go!
            x = 2 * ROOMS[d] + 2
            if x > p:
                for k in range(p+1, x):
                    if k in blocked:
                        break  # We're blocked by some dude
                else:
                    new_room = room + d
                    new_hall = tuple(e for e in hall if e[0] != p)
                    new_dudes = list(dudes)
                    new_dudes[ROOMS[d]] = new_room
                    new_dudes[-1] = new_hall

                    cost = COSTS[d] * (x - p + (rs - roomlen))
                    yield tuple(new_dudes), cost

            else:
                for k in range(p-1, x, -1):
                    if k in blocked:
                        break  # We're blocked by some dude
                else:
                    new_room = room + d
                    new_hall = tuple(e for e in hall if e[0] != p)
                    new_dudes = list(dudes)
                    new_dudes[ROOMS[d]] = new_room
                    new_dudes[-1] = new_hall

                    cost = COSTS[d] * (p - x + rs - roomlen)
                    yield tuple(new_dudes), cost

    # Now see if anyone can leave their room
    for k in range(4):
        room = dudes[k]
        roomlen = len(room)
        if room and any(ROOMS[other] != k for other in room):
            newroom, d = room[:-1], room[-1]
            x = 2 * k + 2
            # Move right
            for p in range(x, 11):
                if p in ILLEGAL:
                    continue
                if p in blocked:
                    break  # Blocked by some dude
                # We can move here
                newhall = list(hall)
                newhall.append((p, d))
                newdudes = list(dudes)
                newdudes[-1] = tuple(sorted(newhall))
                newdudes[k] = newroom

                cost = COSTS[d] * (p - x + 1 + rs - roomlen)
                yield tuple(newdudes), cost
            # Move left
            for p in range(x, -1, -1):
                if p in ILLEGAL:
                    continue
                if p in blocked:
                    break  # Blocked by some dude
                # We can move here
                newhall = list(hall)
                newhall.append((p, d))
                newdudes = list(dudes)
                newdudes[-1] = tuple(sorted(newhall))
                newdudes[k] = newroom

                cost = COSTS[d] * (x - p + 1 + rs - roomlen)
                yield tuple(newdudes), cost


def parse(input):
    lines = input.split("\n")
    dudes = [[] for _ in range(4)]

    for i in range(2):
        for j in range(4):
            dudes[j].append(lines[3 - i][3 + 2 * j])

    parsed1 = tuple("".join(room) for room in dudes) + ((),)

    # Now we "unfold" the map
    lines = lines[:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + lines[3:]
    dudes = [[] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            dudes[j].append(lines[5 - i][3 + 2 * j])

    parsed2 = tuple("".join(room) for room in dudes) + ((),)
    return parsed1, parsed2
