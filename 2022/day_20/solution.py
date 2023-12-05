from collections import deque


def parse(data):
    return list(map(int, data.strip().split("\n")))


def solve(input):
    return part1(input), part2(input)


def part1(input):
    result = mix(input)
    return getnum(result)


def part2(input):
    result = mixmany(input)
    return getnum(result)


def getnum(input):
    result = 0
    for x in range(1000, 4000, 1000):
        result += input[(input.index(0) + x) % len(input)]
    return result


def mixmany(input):
    numbers = [811589153 * i for i in input]
    indices = deque(range(len(input)))

    for _ in range(10):
        for index, number in enumerate(numbers):
            location = indices.index(index)
            indices.rotate(-location)
            indices.popleft()
            indices.rotate(-number)
            indices.appendleft(index)

    return [numbers[i] for i in indices]


def mix(input):
    indices = deque(range(len(input)))

    for index, number in enumerate(input):
        location = indices.index(index)
        indices.rotate(-location)
        indices.popleft()
        indices.rotate(-number)
        indices.appendleft(index)

    return [input[i] for i in indices]
