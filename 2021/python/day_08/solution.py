from collections import defaultdict

LENGTHS = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}


def parse(input):
    result = []
    for line in input.split("\n"):
        if not line.strip():
            continue
        lhs, rhs = line.strip().split("|")
        result.append((lhs.strip().split(), rhs.strip().split()))
    return result


def solve(input):
    return compute1(input), compute2(input)


def compute1(input):
    UNIQ_LENS = {2, 3, 4, 7}
    uniques = 0
    for _, rhs in input:
        for num in rhs:
            if len(num) in UNIQ_LENS:
                uniques += 1

    return uniques


def compute2(input):
    return sum(compute_line(*line) for line in input)


def compute_line(lhs, rhs):
    known = {}
    lhs = ["".join(sorted(n)) for n in lhs]
    rhs = ["".join(sorted(n)) for n in rhs]

    by_length = defaultdict(list)
    for num in lhs:
        by_length[len(num)].append(num)

    known[1] = by_length[2][0]
    known[4] = by_length[4][0]
    known[7] = by_length[3][0]
    known[8] = by_length[7][0]

    # 0, 6, 9
    for num in by_length[6]:
        # Only 9 covers 4 completely
        if set(num).issuperset(known[4]):
            known[9] = num
        # 0 covers 1 completely
        elif set(num).issuperset(known[1]):
            known[0] = num
        # But 6 does not
        else:
            known[6] = num

    # 2, 3, 5
    for num in by_length[5]:
        # Only 3 covers 1 completely
        if set(num).issuperset(known[1]):
            known[3] = num
        # 5 is completely coverd by 6
        elif set(num).issubset(known[6]):
            known[5] = num
        # But 2 is not
        else:
            known[2] = num

    lookup = {v: k for k, v in known.items()}
    digits = [lookup[d] for d in rhs]

    return 1000 * digits[0] + 100 * digits[1] + 10 * digits[2] + digits[3]
