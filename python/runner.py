import importlib
import os
from argparse import ArgumentParser

HERE = os.path.abspath(os.path.dirname(__file__))


# Find and import all the available solutions
solutions = {}
inputs = {}
for d in os.listdir("."):
    if os.path.isdir(d) and os.path.exists(os.path.join(d, "__init__.py")):
        try:
            day = int(d.split("_")[1])
        except (IndexError, ValueError):
            continue

        solutions[day] = importlib.import_module(f"{d}.solution")
        inputs[day] = d + ".txt"

# Run the desired solution on the input
parser = ArgumentParser(description="Run a solution")
parser.add_argument("day", metavar="D", type=int)
parser.add_argument(
    "--input_folder",
    default=os.path.join(HERE, "input"),
    help="path to input folder with files of the form input_01.txt",
)
args = parser.parse_args()

# Solve the problem
try:
    input_file = os.path.join(args.input_folder, inputs[args.day])
    solver = solutions[args.day]
except KeyError:
    print(f"You haven't made a solution for day {args.day} yet!")
    exit(1)

with open(input_file) as f:
    solver.solve(f)
