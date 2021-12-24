from dataclasses import dataclass
from typing import List, Tuple


def parse(input):
    for line in input.strip().split("\n"):
        ins = []
        state, box = line.split()
        ins.append(state)
        for coord in box.split(","):
            a, b = coord[2:].split("..")
            ins.append((int(a), int(b)))

        yield ins


def solve(input):
    input = list(input)
    return len(compute(input)), compute2(input, lim=float("inf"))


def compute(input, lim=50):
    on = set()

    for state, xx, yy, zz in input:
        for x in range(max(xx[0], -lim), min(xx[1], lim) + 1):
            for y in range(max(yy[0], -lim), min(yy[1], lim) + 1):
                for z in range(max(zz[0], -lim), min(zz[1], lim) + 1):
                    if state == "on":
                        on.add((x, y, z))
                    else:
                        on.discard((x, y, z))

    return on


def compute2(input, lim=50):
    on = []

    for state, xx, yy, zz in input:
        cube = Cube(coords=(xx, yy, zz), subcubes=[])
        for prev in on:
            prev.subtract(cube)

        if state == "on":
            on.append(cube)

    return sum(cube.area(lim) for cube in on)


@dataclass
class Cube:

    coords: Tuple[Tuple[int]]
    subcubes: List["Cube"]

    def area(self, lim: int = 50) -> int:
        """Total area not covered by subcubes."""
        naive = 1
        for cmin, cmax in self.coords:
            naive *= (bound(cmax+1, lim) - bound(cmin, lim))

        for subcube in self.subcubes:
            naive -= subcube.area(lim=lim)

        return naive

    def subtract(self, other: "Cube") -> None:
        """Subtract another cube from this one."""
        dims = []

        for cc, dd in zip(self.coords, other.coords):
            if dd[1] < cc[0] or cc[1] < dd[0]:
                # Completely to the left / right
                return
            else:
                # Find the points of cube that lie inside this cube
                dims.append((max(cc[0], dd[0]), min(cc[1], dd[1])))

        for subcube in self.subcubes:
            subcube.subtract(other)

        self.subcubes.append(Cube(tuple(dims), []))


def bound(num, lim=50):
    return max(min(num, lim+1), -lim)
