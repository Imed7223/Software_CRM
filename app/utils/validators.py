import re
from datetime import datetime
from app.models.users import Department


def validate_email(email: str):
    """Valider un email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str):
    """Valider un numéro de téléphone"""
    pattern = r'^(\+33|0)[1-9](\d{2}){4}$'
    cleaned = re.sub(r'[.\s-]', '', phone)
    return bool(re.match(pattern, cleaned))


def validate_date(date_str: str, fmt: str = '%Y-%m-%d'):
    """Valider une date"""
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


def validate_datetime(datetime_str: str, fmt: str = '%Y-%m-%d %H:%M'):
    """Valider un datetime"""
    try:
        datetime.strptime(datetime_str, fmt)
        return True
    except ValueError:
        return False


def validate_amount(amount: str):
    """Valider un montant"""
    try:
        return float(amount) >= 0
    except ValueError:
        return False


def validate_integer(value: str):
    """Valider un entier"""
    try:
        int(value)
        return True
    except ValueError:
        return False


def clean_phone_number(phone: str):
    """Nettoyer un numéro de téléphone"""
    return re.sub(r'[.\s-]', '', phone)


def format_phone_number(phone: str):
    """Formater un numéro de téléphone"""
    cleaned = clean_phone_number(phone)
    if len(cleaned) == 10:
        return f"{cleaned[0:2]} {cleaned[2:4]} {cleaned[4:6]} {cleaned[6:8]} {cleaned[8:10]}"
    return phone


def validate_department(dept: str):
    """Valider un département"""
    try:
        Department(dept.upper())
        return True
    except ValueError:
        return False
