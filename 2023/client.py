from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = (HERE / "data").resolve()
try:
    with open(DATA / "session.txt") as f:
        COOKIES = {"session": f.read().strip()}
except Exception:
    print("Please place your session cookie in data/session.txt")
    exit(1)


def get_day(day):
    filepath = DATA / (day + ".txt")
    if filepath.exists():
        with open(filepath) as f:
            return f.read()

    # Download and cache the input
    import requests
    resp = requests.get(
        f"https://adventofcode.com/2023/day/{int(day)}/input", cookies=COOKIES
    )
    resp.raise_for_status()
    resp_data = resp.text

    with open(filepath, "w") as f:
        f.write(resp_data)

    return resp_data
