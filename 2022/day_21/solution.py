from operator import add, eq, floordiv as div, mul, sub

OPERATORS = {"+": add, "-": sub, "*": mul, "/": div}


def parse(data):
    monkeys = {}
    for line in data.strip().split("\n"):
        monkey, instruction = line.strip().split(": ")
        for k, v in OPERATORS.items():
            if k in instruction:
                monkeys[monkey] = (
                    v, [m.strip() for m in instruction.split(k)]
                )
                break
        else:
            monkeys[monkey] = int(instruction)

    return monkeys


def solve(input):
    return part1(input), part2(input)


def part1(input):
    return eval("root", input.copy())


def part2(input):
    input["humn"] = "humn"
    input["root"] = (eq, input["root"][1])
    formula = eval("root", input)

    left, right = formula[1]
    if isinstance(left, int):
        target, formula = left, right
    else:
        formula, target = left, right

    while formula != "humn":
        op, (left, right) = formula

        if isinstance(left, int):
            formula = right
            if op == add:
                target = target - left
            elif op == sub:
                target = left - target
            elif op == mul:
                target = target // left
            else:
                target = left // target
        elif isinstance(right, int):
            formula = left
            if op == add:
                target = target - right
            elif op == sub:
                target = target + right
            elif op == mul:
                target = target // right
            else:
                target = target * right

    return target


def eval(monkey, monkeys):
    value = monkeys[monkey]
    if value == "humn" or isinstance(value, int):
        return value

    operator, others = value
    for other in others:
        monkeys[other] = eval(other, monkeys)

    left, right = monkeys[others[0]], monkeys[others[1]]
    if not (isinstance(left, int) and isinstance(right, int)):
        return (operator, (left, right))  # formula

    return int(operator(left, right))  # value
