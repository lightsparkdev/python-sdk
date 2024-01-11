# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity


@dataclass
class ChannelSnapshot(Entity):
    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    local_balance: Optional[CurrencyAmount]

    local_unsettled_balance: Optional[CurrencyAmount]

    remote_balance: Optional[CurrencyAmount]

    remote_unsettled_balance: Optional[CurrencyAmount]

    channel_id: str

    local_channel_reserve: Optional[CurrencyAmount]

    timestamp: datetime
    """The timestamp that was used to query the snapshot of the channel"""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "ChannelSnapshot",
            "channel_snapshot_id": self.id,
            "channel_snapshot_created_at": self.created_at.isoformat(),
            "channel_snapshot_updated_at": self.updated_at.isoformat(),
            "channel_snapshot_local_balance": self.local_balance.to_json()
            if self.local_balance
            else None,
            "channel_snapshot_local_unsettled_balance": self.local_unsettled_balance.to_json()
            if self.local_unsettled_balance
            else None,
            "channel_snapshot_remote_balance": self.remote_balance.to_json()
            if self.remote_balance
            else None,
            "channel_snapshot_remote_unsettled_balance": self.remote_unsettled_balance.to_json()
            if self.remote_unsettled_balance
            else None,
            "channel_snapshot_channel": {"id": self.channel_id},
            "channel_snapshot_local_channel_reserve": self.local_channel_reserve.to_json()
            if self.local_channel_reserve
            else None,
            "channel_snapshot_timestamp": self.timestamp.isoformat(),
        }


FRAGMENT = """
fragment ChannelSnapshotFragment on ChannelSnapshot {
    __typename
    channel_snapshot_id: id
    channel_snapshot_created_at: created_at
    channel_snapshot_updated_at: updated_at
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
    channel_snapshot_remote_balance: remote_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_snapshot_remote_unsettled_balance: remote_unsettled_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_snapshot_channel: channel {
        id
    }
    channel_snapshot_local_channel_reserve: local_channel_reserve {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_snapshot_timestamp: timestamp
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ChannelSnapshot:
    return ChannelSnapshot(
        requester=requester,
        typename="ChannelSnapshot",
        id=obj["channel_snapshot_id"],
        created_at=datetime.fromisoformat(obj["channel_snapshot_created_at"]),
        updated_at=datetime.fromisoformat(obj["channel_snapshot_updated_at"]),
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
        remote_balance=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_remote_balance"]
        )
        if obj["channel_snapshot_remote_balance"]
        else None,
        remote_unsettled_balance=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_remote_unsettled_balance"]
        )
        if obj["channel_snapshot_remote_unsettled_balance"]
        else None,
        channel_id=obj["channel_snapshot_channel"]["id"],
        local_channel_reserve=CurrencyAmount_from_json(
            requester, obj["channel_snapshot_local_channel_reserve"]
        )
        if obj["channel_snapshot_local_channel_reserve"]
        else None,
        timestamp=datetime.fromisoformat(obj["channel_snapshot_timestamp"]),
    )
