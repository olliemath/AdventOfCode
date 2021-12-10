def parse(data):
    return [int(r.strip()) for r in data.split() if r.strip()]


def solve(input):
    return detect_increases(input), detect_increases(window_sum(input, 3))


def detect_increases(nums):
    inums = iter(nums)
    increases = 0

    prev = next(inums)
    for num in inums:
        if num > prev:
            increases += 1
        prev = num

    return increases


def window_sum(nums, size):
    for k in range(len(nums) - size + 1):
        yield sum(nums[k:k+size])
