from app.utils import validate_department, format_phone_number, clean_phone_number, validate_integer, validate_amount, \
    validate_datetime, validate_date, validate_phone, validate_email


def test_validate_email():
    assert validate_email("user@test.com")
    assert not validate_email("bad-email")


def test_validate_phone():
    assert validate_phone("0612345678")
    assert validate_phone("+33612345678")
    assert not validate_phone("012345678")


def test_validate_date_and_datetime():
    assert validate_date("2025-12-31")
    assert validate_datetime("2025-12-31 23:59")


def test_validate_amount():
    assert validate_amount("0")
    assert validate_amount("10.5")
    assert not validate_amount("-1")


def test_validate_integer():
    assert validate_integer("0")
    assert validate_integer("42")
    assert not validate_integer("3.14")


def test_clean_and_format_phone_number():
    assert clean_phone_number("06.12 34-56 78") == "0612345678"
    assert format_phone_number("06.12 34-56 78") == "06 12 34 56 78"


def test_validate_department():
    assert validate_department("sales")
    assert validate_department("SUPPORT")
    assert not validate_department("unknown")
