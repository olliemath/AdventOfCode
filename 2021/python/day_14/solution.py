from collections import Counter, defaultdict


def parse(input):
    lines = input.strip().split("\n")
    template = lines[0].strip()
    subst = dict(
        ln.strip().split(" -> ") for ln in lines[2:] if ln.strip()
    )

    return template, subst


def solve(input):
    return compute(*input), compute(*input, steps=40)


def compute(template, subst, steps=10):
    pairs, counts = init_pair_count(template)
    for _ in range(steps):
        pairs, counts = step(pairs, counts, subst)

    return max(counts.values()) - min(counts.values())


def init_pair_count(template):
    counts = Counter(template)
    pairs = defaultdict(int)
    for k in range(len(template) - 1):
        pairs[template[k:k+2]] += 1

    return pairs, counts


def step(pairs, counts, subst):
    new_pairs = defaultdict(int)
    new_counts = defaultdict(int, counts)

    for pair, num in pairs.items():
        if pair in subst:
            mid = subst[pair]
            # Two new pairs: left-hand and right-hand side
            lh, rh = pair[0] + mid, mid + pair[1]
            new_pairs[lh] += num
            new_pairs[rh] += num
            new_counts[mid] += num
        else:
            new_pairs[pair] += num

    return new_pairs, new_counts
