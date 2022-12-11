def parse(data):
    return data.strip().split("\n")


def solve(input):
    x = 1
    register = [0]

    for ins in input:
        if ins == "noop":
            register.append(0)
        else:
            n = int(ins.split()[1])
            register.extend((0, n))

    sol = 0
    line = ""
    lines = []
    for i, n in enumerate(register):
        x += n
        if ((i + 1 - 20) % 40) == 0:
            sol += (i + 1) * x
        if i and i % 40 == 0:
            lines.append(line)
            line = ""
        if (i % 40) in (x-1, x, x+1):
            line += "#"
        else:
            line += "."

    return sol, "\n      ".join(lines)
