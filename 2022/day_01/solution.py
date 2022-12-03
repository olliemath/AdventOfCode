def parse(data):
    for pack in data.strip().split("\n\n"):
        yield sum(map(int, pack.split("\n")))


def solve(input):
    amounts = sorted(input, reverse=True)
    return amounts[0], sum(amounts[:3])
