# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class ChannelSnapshot:
    requester: Requester

    local_balance: Optional[CurrencyAmount]

    local_unsettled_balance: Optional[CurrencyAmount]

    local_channel_reserve: Optional[CurrencyAmount]


FRAGMENT = """
fragment ChannelSnapshotFragment on ChannelSnapshot {
    __typename
    channel_snapshot_local_balance: local_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_snapshot_local_unsettled_balance: local_unsettled_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_snapshot_local_channel_reserve: local_channel_reserve {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ChannelSnapshot:
    return ChannelSnapshot(
        requester=requester,
        local_balance=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_local_balance"]
        )
        if obj["channel_snapshot_local_balance"]
        else None,
        local_unsettled_balance=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_local_unsettled_balance"]
        )
        if obj["channel_snapshot_local_unsettled_balance"]
        else None,
        local_channel_reserve=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_local_channel_reserve"]
        )
        if obj["channel_snapshot_local_channel_reserve"]
        else None,
    )
