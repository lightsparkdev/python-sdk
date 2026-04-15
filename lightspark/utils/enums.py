from __future__ import annotations

from enum import Enum
from typing import TypeVar

T = TypeVar("T", bound=Enum)


def parse_enum(enum_type: type[T], value: str) -> T:
    try:
        return enum_type[value]
    except KeyError:
        return enum_type["___FUTURE_VALUE___"]


def parse_enum_list(enum_type: type[T], values: list[str]) -> list[T]:
    return [parse_enum(enum_type, value) for value in values]


def parse_enum_optional(enum_type: type[T], value: str | None) -> T | None:
    return parse_enum(enum_type, value) if value else None


def parse_optional_list_of_enums(
    enum_type: type[T], values: list[str] | None
) -> list[T] | None:
    return parse_enum_list(enum_type, values) if values else None


def parse_list_of_optional_enums(
    enum_type: type[T], values: list[str | None]
) -> list[T | None]:
    return [parse_enum_optional(enum_type, value) for value in values]


def parse_optional_list_of_optional_enums(
    enum_type: type[T], values: list[str | None] | None
) -> list[T | None] | None:
    return parse_list_of_optional_enums(enum_type, values) if values else None
