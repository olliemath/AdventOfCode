from __future__ import annotations

from collections import Counter

WEIGHTS = {
    (5,): "6",
    (1, 4): "5",
    (2, 3): "4",
    (1, 1, 3): "3",
    (1, 2, 2): "2",
    (1, 1, 1, 2): "1",
    (1, 1, 1, 1, 1): "0",
}


def parse(data):
    chunks = [chunk.split() for chunk in data.strip().split("\n")]
    for chunk in chunks:
        chunk[0] = (
            chunk[0]
            # make T/J/Q/K/A sortable - actual names don't matter
            .replace("A", "E")
            .replace("K", "D")
            .replace("Q", "C")
            .replace("J", "B")
            .replace("T", "A")
        )
        chunk[1] = int(chunk[1])
    return chunks


def solve(input):
    input2 = [(p[0].replace("B", "1"), p[1]) for p in input]
    return get_score(input, weight1), get_score(input2, weight2)


def get_score(input, weightfunc):
    score = 0
    for rank, (_, bid) in enumerate(
        sorted((weightfunc(hand), bid) for hand, bid in input)
    ):
        score += (rank + 1) * bid

    return score


def weight1(hand: str) -> str:
    weight = WEIGHTS[tuple(sorted(Counter(hand).values()))]
    return weight + hand


def weight2(hand: str) -> str:
    freqs = Counter(hand)
    if "1" in freqs and len(freqs) > 1:
        # find the most frequent item which is not a joker
        candidate = max((v, k) for k, v in freqs.items() if k != "1")[1]
        freqs[candidate] += freqs.pop("1")

    weight = WEIGHTS[tuple(sorted(freqs.values()))]
    return weight + hand
