import itertools


def parse_expenses(lines):
    for l in lines:
        if l.strip().isnumeric():
            yield int(l.strip())


def find_tuple(expenses, n=2):
    # Can you do any better than O(m^(n-1))?
    expenses = set(expenses)

    for tup in itertools.product(*itertools.tee(iter(expenses), n-1)):
        if 2020 - sum(tup) in expenses:
            return (2020 - sum(tup), *tup)


def get_prod(lines, n=2):
    tup = find_tuple(parse_expenses(lines), n=n)
    assert sum(tup) == 2020  # sanity check

    result = 1
    for value in tup:
        result *= value
    return result



def solve(input):
    lines = list(input)
    print("Pair:", get_prod(lines, 2))
    print("Triple:", get_prod(lines, 3))
