from day_14.solution import init_pair_count, parse, compute, step

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def test_parse():
    template, subst = parse(data)
    assert template == "NNCB"
    assert subst["BB"] == "N"


def test_step():
    template, subst = parse(data)

    pairs, counts = init_pair_count(template)
    assert counts == {"B": 1, "C": 1, "N": 2}
    assert pairs == {"NN": 1, "NC": 1, "CB": 1}

    pairs, counts = step(pairs, counts, subst)
    assert (pairs, counts) == init_pair_count("NCNBCHB")
    pairs, counts = step(pairs, counts, subst)
    assert (pairs, counts) == init_pair_count("NBCCNBBBCBHCB")
    pairs, counts = step(pairs, counts, subst)
    assert (pairs, counts) == init_pair_count("NBBBCNCCNBBNBNBBCHBHHBCHB")
    pairs, counts = step(pairs, counts, subst)
    assert (pairs, counts) == init_pair_count(
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )


def test_compute():
    template, subst = parse(data)
    assert compute(template, subst) == 1588
