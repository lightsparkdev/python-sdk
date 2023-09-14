# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import dataclasses
import json
from abc import ABC
from enum import Enum
from typing import Any, Dict, TypeVar

SELF = TypeVar("SELF", bound="JSONable")


@dataclasses.dataclass
class JSONable(ABC):
    def to_dict(self) -> Dict[str, Any]:
        dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, JSONable):
                value = value.to_dict()
            elif isinstance(value, list):
                value = [
                    item.to_dict() if isinstance(item, JSONable) else item
                    for item in value
                ]
            elif isinstance(value, Enum):
                value = value.name
            dict[self._get_field_name(key)] = value
        return dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def _get_field_name_overrides(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _get_field_name(cls, name: str) -> str:
        name_overrides = cls._get_field_name_overrides()
        if name in name_overrides:
            return name_overrides[name]
        words = name.split("_")
        return words[0] + "".join(word.title() for word in words[1:])

    @classmethod
    def from_json(cls: "type[SELF]", json_encoded: str) -> SELF:
        data = cls._from_dict(json.loads(json_encoded))
        return cls(**data)

    @classmethod
    def _from_dict(cls, dict: Dict[str, Any]) -> Dict[str, Any]:
        data = {}
        for field in dataclasses.fields(cls):
            value = dict.get(cls._get_field_name(field.name), None)
            if value is None:
                data[field.name] = None
                continue

            field_type = field.type

            # handle Optional field
            if (
                hasattr(field.type, "__args__")
                and len(field.type.__args__) == 2
                and field.type.__args__[-1] is type(None)
            ):
                field_type = field.type.__args__[0]

            if isinstance(value, list) and hasattr(
                field_type.__args__[0], "_from_dict"
            ):
                # handle list
                field_type = field_type.__args__[0]
                data[field.name] = [
                    field_type(**field_type._from_dict(item)) for item in value
                ]
            elif hasattr(field_type, "_from_dict"):
                data[field.name] = field_type(**field_type._from_dict(value))
            elif isinstance(field_type, type) and issubclass(field_type, Enum):
                data[field.name] = field_type[value]
            else:
                data[field.name] = value

        return data
