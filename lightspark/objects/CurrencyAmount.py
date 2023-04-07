# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.exceptions import LightsparkException
from lightspark.objects.CurrencyUnit import CurrencyUnit
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyUnit import CurrencyUnit


@dataclass
class CurrencyAmount:
    """Represents the value and unit for an amount of currency."""

    requester: Requester

    original_value: int
    """The original numeric value for this CurrencyAmount."""

    original_unit: CurrencyUnit
    """The original unit of currency for this CurrencyAmount."""

    preferred_currency_unit: CurrencyUnit
    """The unit of user's preferred currency."""

    preferred_currency_value_rounded: int
    """The rounded numeric value for this CurrencyAmount in the very base level of user's preferred currency. For example, for USD, the value will be in cents."""

    preferred_currency_value_approx: float
    """The approximate float value for this CurrencyAmount in the very base level of user's preferred currency. For example, for USD, the value will be in cents."""

    _CONVERSION_MAP = {
        CurrencyUnit.BITCOIN: {
            CurrencyUnit.BITCOIN: lambda v: v,
            CurrencyUnit.MICROBITCOIN: lambda v: v * 1_000_000,
            CurrencyUnit.MILLIBITCOIN: lambda v: v * 1000,
            CurrencyUnit.MILLISATOSHI: lambda v: v * 100_000_000_000,
            CurrencyUnit.NANOBITCOIN: lambda v: v * 1_000_000_000,
            CurrencyUnit.SATOSHI: lambda v: v * 100_000_000,
        },
        CurrencyUnit.MICROBITCOIN: {
            CurrencyUnit.BITCOIN: lambda v: round(v / 1_000_000),
            CurrencyUnit.MICROBITCOIN: lambda v: v,
            CurrencyUnit.MILLIBITCOIN: lambda v: round(v / 1000),
            CurrencyUnit.MILLISATOSHI: lambda v: v * 100_000,
            CurrencyUnit.NANOBITCOIN: lambda v: v * 1000,
            CurrencyUnit.SATOSHI: lambda v: v * 100,
        },
        CurrencyUnit.MILLIBITCOIN: {
            CurrencyUnit.BITCOIN: lambda v: round(v / 1_000),
            CurrencyUnit.MICROBITCOIN: lambda v: v * 1000,
            CurrencyUnit.MILLIBITCOIN: lambda v: v,
            CurrencyUnit.MILLISATOSHI: lambda v: v * 100_000_000,
            CurrencyUnit.NANOBITCOIN: lambda v: v * 1_000_000,
            CurrencyUnit.SATOSHI: lambda v: v * 100_000,
        },
        CurrencyUnit.MILLISATOSHI: {
            CurrencyUnit.BITCOIN: lambda v: round(v / 100_000_000_000),
            CurrencyUnit.MICROBITCOIN: lambda v: round(v / 100_000),
            CurrencyUnit.MILLIBITCOIN: lambda v: round(v / 100_000_000),
            CurrencyUnit.MILLISATOSHI: lambda v: v,
            CurrencyUnit.NANOBITCOIN: lambda v: round(v / 100),
            CurrencyUnit.SATOSHI: lambda v: round(v / 1000),
        },
        CurrencyUnit.NANOBITCOIN: {
            CurrencyUnit.BITCOIN: lambda v: round(v / 1_000_000_000),
            CurrencyUnit.MICROBITCOIN: lambda v: round(v / 1000),
            CurrencyUnit.MILLIBITCOIN: lambda v: round(v / 1_000_000),
            CurrencyUnit.MILLISATOSHI: lambda v: v * 100,
            CurrencyUnit.NANOBITCOIN: lambda v: v,
            CurrencyUnit.SATOSHI: lambda v: round(v / 10),
        },
        CurrencyUnit.SATOSHI: {
            CurrencyUnit.BITCOIN: lambda v: round(v / 100_000_000),
            CurrencyUnit.MICROBITCOIN: lambda v: round(v / 100),
            CurrencyUnit.MILLIBITCOIN: lambda v: round(v / 100_000),
            CurrencyUnit.MILLISATOSHI: lambda v: v * 1000,
            CurrencyUnit.NANOBITCOIN: lambda v: v * 10,
            CurrencyUnit.SATOSHI: lambda v: v,
        },
    }

    def convert_to(self, unit: CurrencyUnit) -> "CurrencyAmount":
        try:
            conversion_fn = self._CONVERSION_MAP[self.original_unit][unit]
        except KeyError as e:
            raise LightsparkException(
                "CONVERSION_ERROR",
                f"Cannot convert from {self.original_unit} to {unit}",
            ) from e
        return CurrencyAmount(
            requester=self.requester,
            original_unit=self.original_unit,
            original_value=self.original_value,
            preferred_currency_value_rounded=conversion_fn(self.original_value),
            preferred_currency_value_approx=conversion_fn(self.original_value),
            preferred_currency_unit=unit,
        )


FRAGMENT = """
fragment CurrencyAmountFragment on CurrencyAmount {
    __typename
    currency_amount_original_value: original_value
    currency_amount_original_unit: original_unit
    currency_amount_preferred_currency_unit: preferred_currency_unit
    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> CurrencyAmount:
    return CurrencyAmount(
        requester=requester,
        original_value=obj["currency_amount_original_value"],
        original_unit=parse_enum(CurrencyUnit, obj["currency_amount_original_unit"]),
        preferred_currency_unit=parse_enum(
            CurrencyUnit, obj["currency_amount_preferred_currency_unit"]
        ),
        preferred_currency_value_rounded=obj[
            "currency_amount_preferred_currency_value_rounded"
        ],
        preferred_currency_value_approx=obj[
            "currency_amount_preferred_currency_value_approx"
        ],
    )
