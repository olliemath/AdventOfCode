from collections import defaultdict


def parse(input):
    return [int(line.split()[-1]) for line in input.strip().split("\n")]


def solve(input):
    return compute(input), max(compute2(input))


def compute(input):
    p1, p2 = input
    s1, s2 = 0, 0

    k = 1
    count = 0
    while True:
        mv = 3 * k + 3
        p1 += mv
        p1 = 1 + (p1 - 1) % 10
        k += 3
        count += 3
        k = 1 + (k - 1) % 100
        s1 += p1
        if s1 >= 1000:
            break

        mv = 3 * k + 3
        p2 += mv
        p2 = 1 + (p2 - 1) % 10
        k += 3
        count += 3
        k = 1 + (k - 1) % 100

        s2 += p2
        if s2 >= 1000:
            break

    return min(s1, s2) * count


def compute2(input):
    p1, p2 = input
    s1, s2 = 0, 0

    # Roll 3 times and these are your outcomes:
    roll_possibilities = {
        3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1
    }
    wins1 = 0
    wins2 = 0

    paths = {(p1, 0, p2, 0): 1}

    while paths:
        newpaths = defaultdict(int)
        for (p1, s1, p2, s2), n in paths.items():
            for r1, m1 in roll_possibilities.items():
                pp1 = p1 + r1
                pp1 = 1 + (pp1 - 1) % 10
                ss1 = s1 + pp1
                if ss1 >= 21:
                    wins1 += n * m1
                    continue

                for r2, m2 in roll_possibilities.items():
                    pp2 = p2 + r2
                    pp2 = 1 + (pp2 - 1) % 10
                    ss2 = s2 + pp2
                    if ss2 >= 21:
                        wins2 += n * m1 * m2
                        continue
                    else:
                        newpaths[(pp1, ss1, pp2, ss2)] += n * m1 * m2

        paths = newpaths

    return wins1, wins2
