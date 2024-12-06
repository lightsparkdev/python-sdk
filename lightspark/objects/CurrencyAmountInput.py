# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.utils.enums import parse_enum

from .CurrencyUnit import CurrencyUnit


@dataclass
class CurrencyAmountInput:

    value: int

    unit: CurrencyUnit

    def to_json(self) -> Mapping[str, Any]:
        return {
            "currency_amount_input_value": self.value,
            "currency_amount_input_unit": self.unit.value,
        }


def from_json(obj: Mapping[str, Any]) -> CurrencyAmountInput:
    return CurrencyAmountInput(
        value=obj["currency_amount_input_value"],
        unit=parse_enum(CurrencyUnit, obj["currency_amount_input_unit"]),
    )
