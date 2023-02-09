from mkpkg.lib.helpers import ordinal


def test_ordinal_st():
    assert ordinal(1) == "1st"
    assert ordinal(21) == "21st"
    assert ordinal(31) == "31st"
    assert ordinal(51) == "51st"


def test_ordinal_nd():
    assert ordinal(2) == "2nd"
    assert ordinal(22) == "22nd"
    assert ordinal(32) == "32nd"
    assert ordinal(42) == "42nd"


def test_ordinal_rd():
    assert ordinal(3) == "3rd"
    assert ordinal(23) == "23rd"
    assert ordinal(33) == "33rd"
    assert ordinal(43) == "43rd"


def test_ordinal_th():
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
