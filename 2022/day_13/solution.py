import itertools
import json


def parse(data):
    pairs = data.strip().split("\n\n")
    for pair in pairs:
        left, right = pair.strip().split()
        yield json.loads(left), json.loads(right)


def solve(input):
    input = [(Packet(left), Packet(right)) for left, right in input]
    return part1(input), part2(input)


def part1(input):
    in_order = []
    for k, pair in enumerate(input):
        if pair[0] < pair[1]:
            in_order.append(k + 1)
    return sum(in_order)


def part2(input):
    dividers = (Packet([[2]]), Packet([[6]]))
    packets = itertools.chain(dividers, *input)
    ordered = sorted(packets)
    first_ix = 1 + ordered.index(dividers[0])
    secnd_ix = 1 + ordered.index(dividers[1])
    return first_ix * secnd_ix


class Packet:
    def __init__(self, body):
        self.body = body

    def __lt__(self, other):
        return self.less(self.body, other.body)

    @classmethod
    def less(cls, left, right):
        for li, ri in itertools.zip_longest(left, right):
            if li is None:
                return True
            elif ri is None:
                return False
            elif isinstance(li, int) and isinstance(ri, int):
                if li < ri:
                    return True
                elif li > ri:
                    return False
            elif isinstance(li, int) and isinstance(ri, list):
                li = [li]
            elif isinstance(li, list) and isinstance(ri, int):
                ri = [ri]

            if isinstance(li, list) and isinstance(ri, list):
                if (elt_less := cls.less(li, ri)) is not None:
                    return elt_less
