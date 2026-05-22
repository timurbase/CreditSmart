"""
CreditSmart uchun maxsus shablon filtrlari.

Filtrlari:
    - format_currency: Valyuta formatida ko'rsatish (masalan: 50 000 000 so'm)
    - format_percent: Foiz formatida ko'rsatish (masalan: 24.5%)
    - format_number: Ming ajratgichli raqam formati (masalan: 1 234 567)
"""

from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter(name='format_currency')
def format_currency(value):
    """Raqamni valyuta formatiga o'tkazish.

    50000000 → "50 000 000 so'm"

    Args:
        value: Raqamli qiymat (int, float, Decimal, str)

    Returns:
        str: Formatlangan valyuta qiymati yoki asl qiymat (xatolik bo'lsa)
    """
    try:
        number = Decimal(str(value)).quantize(Decimal('1'))
        # Ming ajratgichini qo'shish (bo'sh joy bilan)
        formatted = _add_thousand_separator(int(number))
        return f"{formatted} so'm"
    except (InvalidOperation, ValueError, TypeError):
        return value


@register.filter(name='format_percent')
def format_percent(value):
    """Raqamni foiz formatiga o'tkazish.

    24.5 → "24.5%"

    Args:
        value: Raqamli qiymat

    Returns:
        str: Formatlangan foiz qiymati
    """
    try:
        number = Decimal(str(value))
        # Keraksiz nollarni olib tashlash
        normalized = number.normalize()
        return f"{normalized}%"
    except (InvalidOperation, ValueError, TypeError):
        return value


@register.filter(name='format_number')
def format_number(value):
    """Raqamga ming ajratgichini qo'shish.

    1234567 → "1 234 567"

    Args:
        value: Raqamli qiymat

    Returns:
        str: Ming ajratgichli raqam
    """
    try:
        number = Decimal(str(value))

        # Butun va kasr qismlarini ajratish
        if number == number.to_integral_value():
            return _add_thousand_separator(int(number))
        else:
            integer_part = int(number)
            decimal_part = str(number).split('.')[1]
            formatted_integer = _add_thousand_separator(integer_part)
            return f"{formatted_integer}.{decimal_part}"

    except (InvalidOperation, ValueError, TypeError):
        return value


def _add_thousand_separator(number):
    """Butun songa ming ajratgichini (bo'sh joy) qo'shish.

    Args:
        number: Butun son

    Returns:
        str: Formatlangan raqam (masalan: "1 234 567")
    """
    is_negative = number < 0
    number = abs(number)

    # Python'ning format funksiyasidan foydalanish
    formatted = f"{number:,}".replace(',', ' ')

    if is_negative:
        formatted = f"-{formatted}"

    return formatted
