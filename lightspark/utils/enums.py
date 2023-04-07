from enum import Enum
from typing import List, Optional, TypeVar, Type

T = TypeVar("T", bound=Enum)


def parse_enum(enum_type: Type[T], value: str) -> T:
    try:
        return enum_type[value]
    except KeyError:
        return enum_type["___FUTURE_VALUE___"]


def parse_enum_list(enum_type: Type[T], values: List[str]) -> List[T]:
    return list(map(lambda value: parse_enum(enum_type, value), values))


def parse_enum_optional(enum_type: Type[T], value: Optional[str]) -> Optional[T]:
    return parse_enum(enum_type, value) if value else None


def parse_optional_list_of_enums(
    enum_type: Type[T], values: Optional[List[str]]
) -> Optional[List[T]]:
    return parse_enum_list(enum_type, values) if values else None


def parse_list_of_optional_enums(
    enum_type: Type[T], values: List[Optional[str]]
) -> List[Optional[T]]:
    return list(map(lambda value: parse_enum_optional(enum_type, value), values))


def parse_optional_list_of_optional_enums(
    enum_type: Type[T], values: Optional[List[Optional[str]]]
) -> Optional[List[Optional[T]]]:
    return parse_list_of_optional_enums(enum_type, values) if values else None
