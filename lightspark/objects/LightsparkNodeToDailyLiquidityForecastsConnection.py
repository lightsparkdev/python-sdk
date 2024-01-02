# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping

from lightspark.objects.LightningPaymentDirection import LightningPaymentDirection
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .DailyLiquidityForecast import DailyLiquidityForecast
from .DailyLiquidityForecast import from_json as DailyLiquidityForecast_from_json
from .LightningPaymentDirection import LightningPaymentDirection


@dataclass
class LightsparkNodeToDailyLiquidityForecastsConnection:
    requester: Requester

    from_date: datetime

    to_date: datetime

    direction: LightningPaymentDirection

    entities: List[DailyLiquidityForecast]
    """The daily liquidity forecasts for the current page of this connection."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "lightspark_node_to_daily_liquidity_forecasts_connection_from_date": self.from_date,
            "lightspark_node_to_daily_liquidity_forecasts_connection_to_date": self.to_date,
            "lightspark_node_to_daily_liquidity_forecasts_connection_direction": self.direction.value,
            "lightspark_node_to_daily_liquidity_forecasts_connection_entities": [
                e.to_json() for e in self.entities
            ],
        }


FRAGMENT = """
fragment LightsparkNodeToDailyLiquidityForecastsConnectionFragment on LightsparkNodeToDailyLiquidityForecastsConnection {
    __typename
    lightspark_node_to_daily_liquidity_forecasts_connection_from_date: from_date
    lightspark_node_to_daily_liquidity_forecasts_connection_to_date: to_date
    lightspark_node_to_daily_liquidity_forecasts_connection_direction: direction
    lightspark_node_to_daily_liquidity_forecasts_connection_entities: entities {
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
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> LightsparkNodeToDailyLiquidityForecastsConnection:
    return LightsparkNodeToDailyLiquidityForecastsConnection(
        requester=requester,
        from_date=obj[
            "lightspark_node_to_daily_liquidity_forecasts_connection_from_date"
        ],
        to_date=obj["lightspark_node_to_daily_liquidity_forecasts_connection_to_date"],
        direction=parse_enum(
            LightningPaymentDirection,
            obj["lightspark_node_to_daily_liquidity_forecasts_connection_direction"],
        ),
        entities=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: DailyLiquidityForecast_from_json(requester, e),
                obj["lightspark_node_to_daily_liquidity_forecasts_connection_entities"],
            )
        ),
    )
