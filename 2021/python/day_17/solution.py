def parse(input):
    xs, ys = input.strip().split(": ")[1].split(", ")
    xs = xs.split("=")[1]
    ys = ys.split("=")[1]
    xmin, xmax = map(int, xs.split(".."))
    ymin, ymax = map(int, ys.split(".."))
    return (xmin, xmax, ymin, ymax)


def solve(input):
    paths = find_paths(input)
    best = max(vy for _, vy in paths)
    return best * (best + 1) // 2, len(paths)


def find_paths(box):
    x_inter = find_x_inter(box)
    y_inter = find_y_inter(box)

    paths = []
    # Find any time intervals where both x and y intersect the box
    for vx, tx_inters in x_inter.items():
        for vy, ty_inters in y_inter.items():
            if ty_inters[0] <= tx_inters[0] <= ty_inters[1]:
                paths.append((vx, vy))
            elif ty_inters[0] <= tx_inters[1] <= ty_inters[1]:
                paths.append((vx, vy))
            elif tx_inters[0] <= ty_inters[0] and ty_inters[1] <= tx_inters[1]:
                paths.append((vx, vy))

    return paths


def find_x_inter(box):
    # For each vx, up to the first one to overshoot, find the points at which
    # it intersects the box
    result = {}
    for vx0 in range(1, box[1] + 1):
        intersections = []
        vx = vx0
        x = 0
        t = 0
        while x <= box[1] and vx != 0:
            x += vx
            t += 1
            vx = max(vx - 1, 0)
            if box[0] <= x <= box[1]:
                intersections.append(t)
                if vx == 0:
                    intersections.append(float("inf"))

        if intersections:
            result[vx0] = (min(intersections), max(intersections))

    return result


def find_y_inter(box):
    # If you shoot up at vy, it takes 2*vy+1 to get back down to 0
    # at which point you have velocity -vy-1
    # We know we'll overshoot the box if -vy-1 < ymin, i.e. if
    # vy > -ymin-1

    result = {}
    for vy0 in range(-box[2]):
        intersections = []
        vy = -vy0 - 1
        y = 0
        t = 2 * vy0 + 1
        while y >= box[2]:
            y += vy
            t += 1
            vy -= 1
            if box[2] <= y <= box[3]:
                intersections.append(t)

        if intersections:
            result[vy0] = (min(intersections), max(intersections))

    # We also do the negative y things
    for vy0 in range(box[2], 0):
        intersections = []
        vy = vy0
        y = 0
        t = 0
        while y >= box[2]:
            y += vy
            t += 1
            vy -= 1
            if box[2] <= y <= box[3]:
                intersections.append(t)

        if intersections:
            result[vy0] = (min(intersections), max(intersections))

    return result
