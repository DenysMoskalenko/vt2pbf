from vt2pbf.service.feature import command, zigzag


def test_command_encoding():
    # cmd 1 (MoveTo) with length 2
    assert command(1, 2) == ((2 << 3) | 1)


def test_zigzag_encoding_integers_and_float():
    assert zigzag(0) == 0
    assert zigzag(1) == 2
    assert zigzag(-1) == 1
    # floats are cast to int first
    assert zigzag(1.9) == 2
