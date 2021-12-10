def parse(input):
    return list(map(int, input.strip().split(",")))


def solve(input):
    return compute(input, 80), compute(input, 256)


def compute(input, days):
    buckets = {k: 0 for k in range(9)}
    for i in input:
        buckets[i] += 1

    for _ in range(days):
        new_buckets = {}
        # All fish reduce their days by 1
        for k in range(8):
            new_buckets[k] = buckets[k + 1]

        # Fish spawn after passing 0
        new_buckets[8] = buckets[0]
        new_buckets[6] += buckets[0]

        buckets = new_buckets

    return sum(buckets.values())
