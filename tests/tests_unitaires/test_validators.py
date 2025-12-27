from app.utils import validators


def test_validate_email():
    assert validators.validate_email("user@test.com")
    assert validators.validate_email("user.name+tag@test.co.uk")
    assert not validators.validate_email("bad-email")
    assert not validators.validate_email("user@test")
    assert not validators.validate_email("user@.com")


def test_validate_phone():
    # formats valides français
    assert validators.validate_phone("0612345678")
    assert validators.validate_phone("+33612345678")
    assert validators.validate_phone("06 12 34 56 78")
    assert validators.validate_phone("06.12.34.56.78")
    # invalides
    assert not validators.validate_phone("012345678")      # trop court
    assert not validators.validate_phone("++33612345678")
    assert not validators.validate_phone("abcdefg")


def test_validate_date_and_datetime():
    assert validators.validate_date("2025-12-31")
    assert not validators.validate_date("31/12/2025")

    assert validators.validate_datetime("2025-12-31 23:59")
    assert not validators.validate_datetime("2025-12-31")


def test_validate_amount():
    assert validators.validate_amount("0")
    assert validators.validate_amount("10.5")
    assert not validators.validate_amount("-1")
    assert not validators.validate_amount("abc")


def test_validate_integer():
    assert validators.validate_integer("0")
    assert validators.validate_integer("42")
    assert not validators.validate_integer("3.14")
    assert not validators.validate_integer("abc")


def test_clean_and_format_phone_number():
    raw = "06.12 34-56 78"
    cleaned = validators.clean_phone_number(raw)
    assert cleaned == "0612345678"

    formatted = validators.format_phone_number(raw)
    assert formatted == "06 12 34 56 78"

    # longueur incorrecte -> renvoie l’original
    assert validators.format_phone_number("123") == "123"


def test_validate_department():
    assert validators.validate_department("sales")
    assert validators.validate_department("SUPPORT")
    assert validators.validate_department("management")

    assert not validators.validate_department("unknown")
    assert not validators.validate_department("")
