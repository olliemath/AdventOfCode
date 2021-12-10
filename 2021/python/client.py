from pathlib import Path

import requests

HERE = Path(__file__).parent.resolve()
DATA = (HERE / ".." / "data").resolve()
with open(DATA / "session.txt") as f:
    COOKIES = {"session": f.read().strip()}


def get_day(day):
    filepath = DATA / (day + ".txt")
    if filepath.exists():
        with open(filepath) as f:
            return f.read()

    # Download and cache the input
    resp = requests.get(
        f"https://adventofcode.com/2021/day/{int(day)}/input", cookies=COOKIES
    )
    resp.raise_for_status()
    resp_data = resp.text

    with open(filepath, "w") as f:
        f.write(resp_data)

    return resp_data
