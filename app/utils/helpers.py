def format_currency(value: float) -> str:
    """
    Formats a float value as a currency string.

    >>> format_currency(1234.56)
    '$1,234.56'
    >>> format_currency(0.0)
    '$0.00'
    >>> format_currency(-10.5)
    '-$10.50'
    """
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"


def validate_cedula(cedula: str) -> bool:
    """
    Validates an Ecuadorian cédula length and digit-only check.

    >>> validate_cedula("1712345678")
    True
    >>> validate_cedula("123")
    False
    >>> validate_cedula("abcdefghij")
    False
    """
    return len(cedula) == 10 and cedula.isdigit()
