from __future__ import annotations

from decimal import Decimal, DecimalException, getcontext
from typing import TypeAlias

NUMBER: TypeAlias = int | float | str | Decimal
getcontext().prec = 42


def number_to_decimal(value: NUMBER) -> Decimal:
    try:
        if not isinstance(value, NUMBER):
            raise TypeError()

        if isinstance(value, Decimal):
            return value
        if isinstance(value, str):
            return Decimal(value.replace(",", "."))
        if isinstance(value, float):
            return Decimal(str(value))
        if isinstance(value, int):
            return Decimal(value)
    except DecimalException:
        raise ValueError(f"Input format error: can't parse '{value}' to a number")


def beautify_decimal(value: Decimal, quantize: bool = True) -> str:
    if quantize:
        value = value.quantize(Decimal("1E-17"))
    value = value.normalize()
    if value == 0:
        return "0"
    return value.to_eng_string()
