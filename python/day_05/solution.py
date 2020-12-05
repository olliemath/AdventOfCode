def parse_boarding_pass(input):
    raw_row, raw_col = input[:7], input[7:]
    bin_row = raw_row.replace("F", "0").replace("B", "1")
    bin_col = raw_col.replace("L", "0").replace("R", "1")

    row, col = int(bin_row, 2), int(bin_col, 2)
    return row, col, row * 8 + col


def parse_boarding_passes(input):
    return [parse_boarding_pass(p) for p in input]


def solve(input):
    highest = max(p[2] for p in parse_boarding_passes(input))
    print("Highest:", highest)
