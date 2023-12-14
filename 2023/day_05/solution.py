from __future__ import annotations


def parse(data):
    chunks = data.strip().split("\n\n")
    seeds = list(map(int, chunks[0].strip().split(":")[1].split()))

    parsed = []
    for chunk in chunks[1:]:
        lines = chunk.strip().split("\n")
        parsed.append(
            [list(map(int, line.strip().split())) for line in lines[1:]]
        )

    return seeds, parsed


def solve(input):
    return min(part1(input)), part2(input)


def part1(input):
    seeds, maps = input

    for seed in seeds:
        for map_ in maps:
            for dest, source, length in map_:
                if source <= seed <= source + length:
                    seed += dest - source
                    break

        yield seed


def part2(input):
    seeds, maps = input

    ranges = [
        (seed_start, seed_start + seed_len)
        for seed_start, seed_len in zip(seeds[::2], seeds[1::2], strict=False)
    ]
    maps = [sorted(map_, key=lambda m: m[1]) for map_ in maps]

    for map_ in maps:
        ranges = map_ranges(ranges, map_)

    return min(r[0] for r in ranges)


def map_ranges(ranges, map_):
    for start, end in ranges:
        for range in map_range(start, end, map_):
            yield range


def map_range(start, end, map_):
    result = []

    for submap in map_:
        mapped, fully_mapped = map_range_once(start, end, submap)
        if fully_mapped:
            result.extend(mapped)
            break
        else:
            result.extend(mapped[:-1])
            start, end = mapped[-1]
    else:
        result.append((start, end))

    return result


def map_range_once(start, end, submap):
    dest, source, length = submap
    result = []
    fully_mapped = False

    if start < source:
        if end <= source:
            result.append((start, end))
            fully_mapped = True

        else:
            result.append((start, source))
            result.append((dest, min(end, source + length) + dest - source))

            if end > source + length:
                result.append((source + length, end))
            else:
                fully_mapped = True

    elif start < source + length:
        result.append((start + dest - source, min(end, source + length) + dest - source))

        if end > source + length:
            result.append((source + length, end))
        else:
            fully_mapped = True

    else:
        result.append((start, end))
        fully_mapped = False

    return result, fully_mapped
