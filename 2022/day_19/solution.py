import math
import re


PREFERENCE = ("ore", "clay", "obsidian", "geode")
PHI = (1 + math.sqrt(5)) / 2


def parse(data):
    rex = re.compile(
        r"Each ([a-z]+) robot costs (\d+) ([a-z]+)( and (\d+) ([a-z]+))?."
    )

    blueprints = []
    for line in data.strip().split("\n"):
        blueprint = {}
        for match in rex.findall(line):
            blueprint[match[0]] = {
                match[k+1]: int(match[k])
                for k in (1, 4) if match[k]
            }
        blueprints.append(blueprint)

    return blueprints


def solve(input):
    return part1(input), part2(input)


def part1(input):
    result = 0
    for k, blueprint in enumerate(input):
        result += (k + 1) * best(blueprint=blueprint)

    return result


def part2(input):
    result = 1
    for blueprint in input[:3]:
        result *= best(blueprint=blueprint, N=32)

    return result


def best(blueprint, N=24):
    robots = {k: 0 for k in blueprint} | {"ore": 1}
    resources = {k: 0 for k in blueprint} | {"ore": 1}
    paths = [[(robots, resources, set())]]

    # More than this many robots will not help us build faster
    # since we can only build max 1 robot per turn
    needed = {
        k: max(v.get(k, 0) for v in blueprint.values()) for k in robots
    }

    for t in range(N - 1, 0, -1):
        # scores = {make_key(p): p[-1][-1] for p in paths}
        newpaths = []
        seen = set()

        for path in paths:
            robots = path[-1][0].copy()
            resources = path[-1][1].copy()
            blocked = path[-1][2]
            # See if we have enough to start building
            to_build = []
            for robot in reversed(PREFERENCE):
                if robot != "geode" and (
                    robots[robot] * t + resources[robot] >= needed[robot] * t
                ):
                    continue

                elif robot in blocked:
                    continue

                requirements = blueprint[robot]
                for k, v in requirements.items():
                    if resources[k] < v:
                        break
                else:
                    to_build.append(robot)
                    if robot == "geode":
                        break

            for r, n in robots.items():
                resources[r] += n

            # Now we can either build this dude or wait
            for building in to_build:
                # try building this dude
                b_robots = robots.copy()
                b_resources = resources.copy()
                b_robots[building] += 1
                for r, n in blueprint[building].items():
                    b_resources[r] -= n
                newpath = path + [(b_robots, b_resources, set())]
                if (key := make_key(newpath, t)) not in seen:
                    seen.add(key)
                    newpaths.append(newpath)

            newpath = path + [(robots, resources, blocked.union(to_build))]
            if (key := make_key(newpath, t)) not in seen:
                seen.add(key)
                newpaths.append(newpath)

        paths = newpaths
        # Aggressive path pruning (not guarenteed to work)
        paths = sorted(
            newpaths,
            key=lambda p: p[-1][1]["geode"],
            reverse=True,
        )[:25_000]

    res = max(paths, key=lambda p: p[-1][1]["geode"])
    return res[-1][1]["geode"]


def make_key(path, t=0):
    robots, resources = path[-1][0], path[-1][1]
    return (
        tuple(robots[k] for k in PREFERENCE[:-1])
        + tuple(resources[k] for k in PREFERENCE[:-1])
        + (resources["geode"] + robots["geode"] * t,)
    )
