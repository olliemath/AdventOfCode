from collections import defaultdict


def parse(data):
    current_path = [""]
    dir_sizes = defaultdict(int)
    total_size = 0
    for line in data.strip().split("\n"):
        line = line.strip()
        if line == "$ cd /":
            current_path = [""]
        elif line == "$ cd ..":
            current_path.pop()
        elif line.startswith("$ cd "):
            # Absolute path to current directory should be unique
            new_path = current_path[-1] + "/" + line.split()[-1]
            current_path.append(new_path)
        elif line.startswith("dir"):
            pass
        elif line.startswith("$ ls"):
            pass
        else:
            filesize = int(line.split()[0])
            total_size += filesize
            for dir in current_path:
                dir_sizes[dir] += filesize

    return dir_sizes, total_size


def solve(input):
    return part1(input), part2(input)


def part1(input):
    dir_sizes, _ = input
    return sum(v for v in dir_sizes.values() if v <= 100000)


def part2(input):
    dir_sizes, total_size = input
    space_needed = 30000000 - (70000000 - total_size)
    return min(v for v in dir_sizes.values() if v >= space_needed)
