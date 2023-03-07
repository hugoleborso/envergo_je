from ..src.index import getNumber
from ..src.index import getLetter


def test_ShouldReturnNumber3():
    returnedValue = getNumber()
    assert returnedValue["number"] == 3

def test_ShouldReturnLetterA():
    returnedValue = getLetter()
    assert returnedValue["letter"] == "a"


