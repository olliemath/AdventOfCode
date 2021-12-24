def parse(input):
    input = input.replace("#", "1").replace(".", "0")
    lines = input.strip().split("\n")

    algo = lines[0]
    image = [list(line) for line in lines[2:]]
    return algo, image


def solve(input):
    algo, image = input
    border = "0"
    image = pad(image, 3, border)
    for k in range(50):
        image, border = compute(algo, image, border)
        image = pad(image, 2, border)
        if k == 1:
            part1 = sum(
                sum(int(c) for c in row[1:-1]) for row in image[1:-1]
            )

    return part1, sum(
        sum(int(c) for c in row[1:-1]) for row in image[1:-1]
    )


def pad(image, n, b="0"):
    # This is a bit of a hack. Basically we want to pad around the edges of
    # the current image so there are at least n rows with the border state
    # b. The easy way to do that is to add n rows each time. But that makes
    # calculations slower. A better way is to "top up" the border by detecting
    # the number of border rows already present.
    current = 0
    for row in image:
        if all(c == b for c in row):
            current += 1
        else:
            break

    current2 = 0
    for row in reversed(image):
        if all(c == b for c in row):
            current2 += 1
        else:
            break

    n -= min(current, current2)

    zeros = [b for _ in range(len(image[0]) + 2 * n)]
    return [zeros for _ in range(n)] + [
        [b for _ in range(n)] + row + [b for _ in range(n)]
        for row in image
    ] + [zeros for _ in range(n)]


def compute(algo, image, border):

    new = [["0" for _ in range(len(image[0]))] for _ in range(len(image))]

    border_shading = algo[int(border * 9, 2)]

    for r in range(len(image)):
        for c in range(len(image[0])):
            new[r][c] = algo[get_binary(image, r, c, border)]

    # Colour the border too
    for row in image:
        row[0] = row[-1] = border_shading

    image[0] = [border_shading for _ in range(len(image[0]))]
    image[-1] = [border_shading for _ in range(len(image[0]))]

    return new, border_shading


def get_binary(image, r, c, border):
    res = []
    for rr in (r-1, r, r+1):
        for cc in (c-1, c, c+1):
            try:
                res.append(image[rr][cc])
            except IndexError:
                res.append(border)

    return int("".join(res), 2)


def print_image(image):
    for row in image:
        print("".join(row[:175]).replace("0", ".").replace("1", "#"))
