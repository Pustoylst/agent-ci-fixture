from calculator import subtract


def test_subtracts_numbers() -> None:
    assert subtract(5, 4) == 1


def test_subtracts_negative_numbers() -> None:
    assert subtract(-2, 3) == -5

