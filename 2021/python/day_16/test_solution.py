from day_16.solution import parse, parse_bytes, solve, sum_versions

from unittest.mock import ANY

data = """D2FE28"""
data2 = """38006F45291200"""
data3 = """EE00D40C823060"""


def test_parse():
    parsed = parse(data)
    assert parsed == "110100101111111000101000"

    parsed = parse(data2)
    assert parsed == (
        "00111000000000000110111101000101001010010001001000000000"
    )


def test_parse_bytes():
    assert parse_bytes(iter(parse(data))) == (6, 4, 2021)


def test_parse_sum_subpackets():
    actual = parse_bytes(iter(parse(data2)))
    assert actual == (1, ANY, [(6, ANY, 10), (2, ANY, 20)])

    actual = parse_bytes(iter(parse(data3)))
    assert actual == (7, ANY, [(2, ANY, 1), (4, ANY, 2), (1, ANY, 3)])

    assert sum_versions(actual) == 7 + 2 + 4 + 1


def test_solve():
    assert solve(parse("8A004A801A8002F478"))[0] == 16
    assert solve(parse("620080001611562C8802118E34"))[0] == 12
    assert solve(parse("C0015000016115A2E0802F182340"))[0] == 23
    assert solve(parse("A0016C880162017C3686B18A3D4780"))[0] == 31


def test_solve2():
    assert solve(parse("C200B40A82"))[1] == 3
    assert solve(parse("04005AC33890"))[1] == 54
    assert solve(parse("880086C3E88112"))[1] == 7
    assert solve(parse("CE00C43D881120"))[1] == 9
    assert solve(parse("D8005AC2A8F0"))[1] == 1
    assert solve(parse("F600BC2D8F"))[1] == 0
    assert solve(parse("9C005AC2F8F0"))[1] == 0
    assert solve(parse("9C0141080250320F1802104A08"))[1] == 1
