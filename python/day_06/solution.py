def parse(input):
    group = []
    for row in input:
        row = row.strip()
        if row:
            group.append(row)
        elif group:
            yield group
            group = []

    if group:
        yield group


def num_yeses_any(input):
    return sum(len(set.union(*map(set, group))) for group in input)



def num_yeses_all(input):
    return sum(len(set.intersection(*map(set, group))) for group in input)


def solve(input):
    print("Yeses:", num_yeses_all(parse(input)))
