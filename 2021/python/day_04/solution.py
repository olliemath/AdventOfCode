import itertools
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Number:
    value: int
    seen: bool = False

    def __hash__(self):
        return self.value


def parse(input):
    lines = [ln.strip() for ln in input.split("\n") if ln.strip()]
    ilines = iter(lines)
    draw = list(map(int, next(ilines).split(",")))

    grids = []
    for _ in range(0, len(lines) - 1, 5):
        grids.append(tuple(
            tuple(map(Number, map(int, ln.split())))
            for ln in itertools.islice(ilines, 5)
        ))

    return draw, grids


def solve(parsed):
    return compute(*parsed)


def compute(draw, grids):
    winning_order = play_bingo(draw, grids)

    winning_number, winning_grid = winning_order[0]
    loosing_number, loosing_grid = winning_order[-1]

    return winning_number * winning_grid, loosing_number * loosing_grid


def play_bingo(draw, grids):
    num_map = defaultdict(list)
    winning_order = []
    won = set()
    left_to_check = grids

    for grid in grids:
        for row in grid:
            for cell in row:
                num_map[cell.value].append(cell)

    for k, d in enumerate(draw):
        for cell in num_map.get(d, []):
            cell.seen = True

        if k < 5:
            continue

        for grid in left_to_check:
            # Check the rows
            for row in grid:
                for cell in row:
                    if not cell.seen:
                        break
                else:
                    winning_order.append((d, sum_grid(grid)))  # bingo!
                    won.add(grid)
                    break
            # Check the columns
            for k in range(5):
                for row in grid:
                    if not row[k].seen:
                        break
                else:
                    winning_order.append((d, sum_grid(grid)))  # bingo!
                    won.add(grid)
                    break

        left_to_check = [g for g in left_to_check if g not in won]
        if not left_to_check:
            break

    return winning_order


def sum_grid(grid):
    return sum(c.value for r in grid for c in r if not c.seen)
