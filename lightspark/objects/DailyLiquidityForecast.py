# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from lightspark.objects.LightningPaymentDirection import LightningPaymentDirection
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .LightningPaymentDirection import LightningPaymentDirection


@dataclass
class DailyLiquidityForecast:
    requester: Requester

    date: datetime
    """The date for which this forecast was generated."""

    direction: LightningPaymentDirection
    """The direction for which this forecast was generated."""

    amount: CurrencyAmount
    """The value of the forecast. It represents the amount of msats that we think will be moved for that specified direction, for that node, on that date."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "daily_liquidity_forecast_date": self.date,
            "daily_liquidity_forecast_direction": self.direction.value,
            "daily_liquidity_forecast_amount": self.amount.to_json(),
        }


FRAGMENT = """
fragment DailyLiquidityForecastFragment on DailyLiquidityForecast {
    __typename
    daily_liquidity_forecast_date: date
    daily_liquidity_forecast_direction: direction
    daily_liquidity_forecast_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> DailyLiquidityForecast:
    return DailyLiquidityForecast(
        requester=requester,
        date=obj["daily_liquidity_forecast_date"],
        direction=parse_enum(
            LightningPaymentDirection, obj["daily_liquidity_forecast_direction"]
        ),
        amount=CurrencyAmount_from_json(
            requester, obj["daily_liquidity_forecast_amount"]
        ),
    )
