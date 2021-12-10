import importlib
import os
import time

from util import print_blue, print_green, print_red, print_yellow, print_header
from client import get_day

print_header("=== Merry Christmas! ===\n")

dirs = sorted(dir for dir in os.listdir(".") if dir.startswith("day_"))

for dir in dirs:
    day = dir.split("_")[1]
    print(f"Day {day}")

    data = get_day(day)
    print_blue("  input obtained")

    module = importlib.import_module(dir + ".solution")
    print_yellow("  parsing")
    parsed = module.parse(data)
    print_red("  solving..")
    t0 = time.time()
    solution = module.solve(parsed)
    t1 = time.time()
    print_green(f"    Solution: {solution}")
    print_red(f"    [{t1-t0:.4f}s]")
    print()
