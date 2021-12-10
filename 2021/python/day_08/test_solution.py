from day_08.solution import parse, compute1, compute2, compute_line


data0 = (
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | "
    "cdfeb fcadb cdfeb cdbaf"
)

data1 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""  # noqa: E501


def test_parse():
    parsed = parse(data0)
    assert len(parsed) == 1
    assert len(parsed[0][0]) == 10
    assert len(parsed[0][1]) == 4


def test_compute1():
    parsed = parse(data1)
    assert compute1(parsed) == 26


def test_compute2():
    parsed = parse(data1)
    assert [compute_line(*line) for line in parsed] == [
        8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315
    ]

    assert compute2(parsed) == 61229
