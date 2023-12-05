import importlib
import os
import time
import sys

from util import print_blue, print_green, print_red, print_yellow, print_header
from client import get_day


print_header("=== Merry Christmas! ===\n")

dirs = sorted(dir for dir in os.listdir(".") if dir.startswith("day_"))
args = sys.argv[1:]

for dir in dirs:
    day = dir.split("_")[1]
    if args and int(day) != int(args[0]):
        continue
    print(f"Day {day}")

    data = get_day(day)
    print_blue("  input obtained")

    module = importlib.import_module(dir + ".solution")
    print_yellow("  parsing")
    t0 = time.time()
    parsed = module.parse(data)
    print_red("  solving..")
    solution = module.solve(parsed)
    t1 = time.time()
    if isinstance(solution, tuple) and len(solution) > 1:
        print_green(f"    Solution:\n      {solution[0]}\n      {solution[1]}")
    else:
        print_green(f"    Solution: {solution}")
    print_red(f"    [{t1-t0:.4f}s]")
    print()
