from statistics import mean, median


def parse(input):
    return sorted(map(int, input.strip().split(",")))


def solve(input):
    return compute(input, l1), compute(input, l2)


def compute(input, norm):
    if norm == l1:
        guess = median(input)
    else:
        guess = mean(input)

    below = int(guess)
    above = int(guess) + 1

    dist_a = sum(norm(i, above) for i in input)
    dist_b = sum(norm(i, below) for i in input)

    return min(dist_a, dist_b)


def l1(a, b):
    return abs(a - b)


def l2(a, b):
    d = abs(a - b)
    return (d * (d + 1)) // 2
