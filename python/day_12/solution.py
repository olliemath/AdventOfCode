def parse(input):
    for row in input:
        row = row.strip()
        yield row[0], int(row[1:])


def follow(instructions):
    lat, lon = 0, 0
    dir = 90

    for ins, value in instructions:
        if ins == "N":
            lat += value
        elif ins == "S":
            lat -= value
        elif ins == "E":
            lon += value
        elif ins == "W":
            lon -= value
        elif ins == "L":
            dir -= value
        elif ins == "R":
            dir += value
        else:
            dir = dir % 360
            if dir < 0:
                dir += 360

            if dir == 0:
                lat += value
            elif dir == 90:
                lon += value
            elif dir == 180:
                lat -= value
            elif dir == 270:
                lon -= value
            else:
                raise ValueError(f"Odd angle: {dir}")

    return abs(lat) + abs(lon)


def solve(input):
    print("Part 1:", follow(parse(input)))
