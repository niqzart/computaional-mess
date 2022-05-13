from decimal import Decimal, InvalidOperation
from enum import Enum
from os.path import isfile
from typing import Callable, TypeVar, Type

t = TypeVar("t")


def checked_input(prompt: str, check: Callable[[str], t | None]) -> t:
    result: t | None = None
    while result is None:
        result = check(input(prompt))
    return result


def input_filename(prompt: str) -> str:
    def filename_check(line: str) -> str | None:
        return line if isfile(line) else None

    return checked_input(prompt, filename_check)


def input_bool(prompt: str) -> bool:
    def bool_check(line: str) -> bool | None:
        try:
            return line.lower() in ("true", "yes", "sure", "go ahead", "yep", "yeah", "y", "+",
                                    "koneshno", "da", "bezuslovno", "razumeets'a")
        except ValueError:
            return None

    return checked_input(prompt, bool_check)


def input_int(prompt: str) -> int:
    def int_check(line: str) -> int | None:
        try:
            return int(line)
        except ValueError:
            return None

    return checked_input(prompt, int_check)


def input_int_range(prompt: str, left: int, right: int) -> int:
    def int_range_check(line: str) -> int | None:
        try:
            result = int(line)
            if left <= result < right:
                return result
            return None
        except ValueError:
            return None

    return checked_input(prompt, int_range_check)


def input_decimal(prompt: str, additional_check: Callable[[Decimal], Decimal | None] = lambda x: x) -> Decimal:
    def decimal_check(line: str) -> Decimal | None:
        try:
            return additional_check(Decimal(line.replace(",", ".")))
        except InvalidOperation:
            return None

    return checked_input(prompt, decimal_check)


e = TypeVar("e", bound=Enum)


def input_menu(menu_items: Type[e], prompt: str) -> e:
    i_to_item: dict[int, e] = {}

    for i, item in enumerate(menu_items.__members__.values()):
        i_to_item[i] = item
        print(f"{i + 1}. {item.value}")

    def int_range_check(line: str) -> e | None:
        try:
            result = int(line) - 1
            if 0 <= result < len(menu_items):
                return i_to_item[result]
            return None
        except ValueError:
            return None

    return checked_input(prompt, int_range_check)
