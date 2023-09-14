# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Dict

from uma.JSONable import JSONable


@dataclass
class Currency(JSONable):
    code: str
    name: str
    symbol: str
    millisatoshi_per_unit: int
    min_sendable: int
    max_sendable: int

    @classmethod
    def _get_field_name_overrides(cls) -> Dict[str, str]:
        return {"millisatoshi_per_unit": "multiplier"}
