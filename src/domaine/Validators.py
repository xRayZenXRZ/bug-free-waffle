from datetime import datetime

def validate_str(field: str, value):
    if not isinstance(value, str):
        raise TypeError(f"l'attribut '{field}' doit être une chaîne de caractère")

def validate_int(field: str, value):
    if not isinstance(value, int):
        raise TypeError(f"l'attribut '{field}' doit être un entier")

def validate_date(field: str, value: str):
    validate_str(field, value)
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"l'attribut '{field}' doit être au format 'yyyy-mm-dd'")

def validate_optional_date(field: str, value):
    if value is not None:
        validate_date(field, value)