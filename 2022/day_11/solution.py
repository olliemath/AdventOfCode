def parse(data):
    return data.strip().split("\n\n")


def solve(input):
    monkeys1 = [Monkey(text) for text in input]
    for _ in range(20):
        round(monkeys1)

    monkeys2 = [Monkey(text) for text in input]
    mod = 1
    for monkey in monkeys2:
        mod *= monkey.div
    for monkey in monkeys2:
        monkey.mod = mod
    for _ in range(10_000):
        round(monkeys2)

    return num(monkeys1), num(monkeys2)


def num(monkeys):
    monkeys = sorted(monkeys, key=lambda m: -m.inspected)
    return monkeys[0].inspected * monkeys[1].inspected


def round(monkeys):
    for monkey in monkeys:
        monkey.process(monkeys)


class Monkey:
    def __init__(self, text):
        self.mod = None
        self.inspected = 0
        _, items, new, div, t, f = text.rstrip().split("\n")

        self.items = list(map(int, items.split(":")[1].split(", ")))
        div = self.div = int(div.split()[-1])
        t = int(t.split()[-1])
        f = int(f.split()[-1])

        self.test = lambda i: f if i % div else t

        if "+" in new:
            if new.endswith("old"):
                self.action = lambda i: i + i
            else:
                x = int(new.split()[-1])
                self.action = lambda i: i + x
        else:
            if new.endswith("old"):
                self.action = lambda i: i * i
            else:
                x = int(new.split()[-1])
                self.action = lambda i: i * x

    def process(self, monkeys):
        self.inspected += len(self.items)
        for item in self.items:
            item = self.action(item)
            if self.mod:
                item = item % self.mod
            else:
                item //= 3
            target = self.test(item)
            monkeys[target].items.append(item)
        self.items = []

    def __repr__(self):
        return f"Monkey({self.items}, inspected={self.inspected})"
