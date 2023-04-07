# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class ChannelToTransactionsConnection:
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    average_fee: Optional[CurrencyAmount]
    """The average fee for the transactions that transited through this channel, according to the filters and constraints of the connection."""

    total_amount_transacted: Optional[CurrencyAmount]
    """The total amount transacted for the transactions that transited through this channel, according to the filters and constraints of the connection."""

    total_fees: Optional[CurrencyAmount]
    """The total amount of fees for the transactions that transited through this channel, according to the filters and constraints of the connection."""


FRAGMENT = """
fragment ChannelToTransactionsConnectionFragment on ChannelToTransactionsConnection {
    __typename
    channel_to_transactions_connection_count: count
    channel_to_transactions_connection_average_fee: average_fee {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_to_transactions_connection_total_amount_transacted: total_amount_transacted {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_to_transactions_connection_total_fees: total_fees {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ChannelToTransactionsConnection:
    return ChannelToTransactionsConnection(
        requester=requester,
        count=obj["channel_to_transactions_connection_count"],
        average_fee=CurrencyAmount_from_json(
            requester, obj["channel_to_transactions_connection_average_fee"]
        )
        if obj["channel_to_transactions_connection_average_fee"]
        else None,
        total_amount_transacted=CurrencyAmount_from_json(
            requester, obj["channel_to_transactions_connection_total_amount_transacted"]
        )
        if obj["channel_to_transactions_connection_total_amount_transacted"]
        else None,
        total_fees=CurrencyAmount_from_json(
            requester, obj["channel_to_transactions_connection_total_fees"]
        )
        if obj["channel_to_transactions_connection_total_fees"]
        else None,
    )
