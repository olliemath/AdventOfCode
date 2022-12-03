from day_24.solution import Machine, solve, parse

data = """inp z
inp x
mul z 3
eql z x"""

data2 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""


def test_parse():
    assert parse(data) == [
        ["inp", "z"],
        ["inp", "x"],
        ["mul", "z", 3],
        ["eql", "z", "x"],
    ]


def test_machine():
    m = Machine(parse(data))
    assert m.run([3, 1]) == 1
    assert m.run([1, 3]) == 0

    m = Machine(parse(data2))
    assert m.run([8 + 4 + 2 + 1]) == 1
    assert m.state["x"] == m.state["y"] == m.state["w"] == 1

    assert m.run([0]) == 0
    assert m.state["x"] == m.state["y"] == m.state["w"] == 0
