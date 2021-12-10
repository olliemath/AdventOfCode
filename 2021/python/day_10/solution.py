def parse(input):
    return input.strip().split("\n")


def solve(input):
    return compute1(input), compute2(input)


def compute1(input):
    scores = list(map(check_line, input))
    return sum(s for s in scores if s is not None)


SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
FLIP = dict(("{}", "()", "[]", "<>"))
FLIP.update(dict(map(reversed, FLIP.items())))
SCORE2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def check_line(line):
    stack = []
    for char in line:
        if char in "({[<":
            stack.append(char)
        elif char in ">)]}":
            try:
                reverse = stack.pop()
                if reverse != FLIP[char]:
                    return SCORE[char]
            except Exception:
                return SCORE[char]


def compute2(input):
    scores = []
    for line in input:
        if check_line(line) is None:
            # Incomplete but valid line
            completion = complete_line(line)
            score = 0
            for char in completion:
                score *= 5
                score += SCORE2[char]
            scores.append(score)

    return sorted(scores)[len(scores) // 2]


def complete_line(line):
    stack = []
    for char in line:
        if char in "({[<":
            stack.append(char)
        elif char in ">)]}":
            reverse = stack.pop()
            assert reverse == FLIP[char]

    solution = []
    while stack:
        solution.append(FLIP[stack.pop()])

    return "".join(solution)
