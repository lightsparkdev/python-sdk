# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.objects.ChannelStatus import ChannelStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_optional

from .ChannelFees import ChannelFees
from .ChannelFees import from_json as ChannelFees_from_json
from .ChannelStatus import ChannelStatus
from .ChannelToTransactionsConnection import ChannelToTransactionsConnection
from .ChannelToTransactionsConnection import (
    from_json as ChannelToTransactionsConnection_from_json,
)
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .TransactionType import TransactionType


@dataclass
class Channel(Entity):
    """An object that represents a payment channel between two nodes in the Lightning Network."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    funding_transaction_id: Optional[str]
    """The transaction that funded the channel upon channel opening."""

    capacity: Optional[CurrencyAmount]
    """The total amount of funds in this channel, including the channel balance on the local node, the channel balance on the remote node and the on-chain fees to close the channel."""

    local_balance: Optional[CurrencyAmount]
    """The channel balance on the local node."""

    local_unsettled_balance: Optional[CurrencyAmount]
    """The channel balance on the local node that is currently allocated to in-progress payments."""

    remote_balance: Optional[CurrencyAmount]
    """The channel balance on the remote node."""

    remote_unsettled_balance: Optional[CurrencyAmount]
    """The channel balance on the remote node that is currently allocated to in-progress payments."""

    unsettled_balance: Optional[CurrencyAmount]
    """The channel balance that is currently allocated to in-progress payments."""

    total_balance: Optional[CurrencyAmount]
    """The total balance in this channel, including the channel balance on both local and remote nodes."""

    status: Optional[ChannelStatus]
    """The current status of this channel."""

    estimated_force_closure_wait_minutes: Optional[int]
    """The estimated time to wait for the channel's hash timelock contract to expire when force closing the channel. It is in unit of minutes."""

    commit_fee: Optional[CurrencyAmount]
    """The amount to be paid in fees for the current set of commitment transactions."""

    fees: Optional[ChannelFees]
    """The fees charged for routing payments through this channel."""

    remote_node_id: Optional[str]
    """If known, the remote node of the channel."""

    local_node_id: str
    """The local Lightspark node of the channel."""

    short_channel_id: Optional[str]
    """The unique identifier of the channel on Lightning Network, which is the location in the chain that the channel was confirmed. The format is <block-height>:<tx-index>:<tx-output>."""
    typename: str

    def get_uptime_percentage(
        self,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
    ) -> Optional[int]:
        json = self.requester.execute_graphql(
            """
query FetchChannelUptimePercentage($entity_id: ID!, $after_date: DateTime, $before_date: DateTime) {
    entity(id: $entity_id) {
        ... on Channel {
            uptime_percentage(, after_date: $after_date, before_date: $before_date)
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "after_date": after_date,
                "before_date": before_date,
            },
        )
        connection = json["entity"]["uptime_percentage"]
        return connection

    def get_transactions(
        self,
        types: Optional[List[TransactionType]] = None,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
    ) -> ChannelToTransactionsConnection:
        json = self.requester.execute_graphql(
            """
query FetchChannelToTransactionsConnection($entity_id: ID!, $types: [TransactionType!], $after_date: DateTime, $before_date: DateTime) {
    entity(id: $entity_id) {
        ... on Channel {
            transactions(, types: $types, after_date: $after_date, before_date: $before_date) {
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
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "types": types,
                "after_date": after_date,
                "before_date": before_date,
            },
        )
        connection = json["entity"]["transactions"]
        return ChannelToTransactionsConnection_from_json(self.requester, connection)


FRAGMENT = """
fragment ChannelFragment on Channel {
    __typename
    channel_id: id
    channel_created_at: created_at
    channel_updated_at: updated_at
    channel_funding_transaction: funding_transaction {
        id
    }
    channel_capacity: capacity {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_local_balance: local_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_local_unsettled_balance: local_unsettled_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_remote_balance: remote_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_remote_unsettled_balance: remote_unsettled_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_unsettled_balance: unsettled_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_total_balance: total_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_status: status
    channel_estimated_force_closure_wait_minutes: estimated_force_closure_wait_minutes
    channel_commit_fee: commit_fee {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_fees: fees {
        __typename
        channel_fees_base_fee: base_fee {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_fees_fee_rate_per_mil: fee_rate_per_mil
    }
    channel_remote_node: remote_node {
        id
    }
    channel_local_node: local_node {
        id
    }
    channel_short_channel_id: short_channel_id
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Channel:
    return Channel(
        requester=requester,
        typename="Channel",
        id=obj["channel_id"],
        created_at=obj["channel_created_at"],
        updated_at=obj["channel_updated_at"],
        funding_transaction_id=obj["channel_funding_transaction"]["id"]
        if obj["channel_funding_transaction"]
        else None,
        capacity=CurrencyAmount_from_json(requester, obj["channel_capacity"])
        if obj["channel_capacity"]
        else None,
        local_balance=CurrencyAmount_from_json(requester, obj["channel_local_balance"])
        if obj["channel_local_balance"]
        else None,
        local_unsettled_balance=CurrencyAmount_from_json(
            requester, obj["channel_local_unsettled_balance"]
        )
        if obj["channel_local_unsettled_balance"]
        else None,
        remote_balance=CurrencyAmount_from_json(
            requester, obj["channel_remote_balance"]
        )
        if obj["channel_remote_balance"]
        else None,
        remote_unsettled_balance=CurrencyAmount_from_json(
            requester, obj["channel_remote_unsettled_balance"]
        )
        if obj["channel_remote_unsettled_balance"]
        else None,
        unsettled_balance=CurrencyAmount_from_json(
            requester, obj["channel_unsettled_balance"]
        )
        if obj["channel_unsettled_balance"]
        else None,
        total_balance=CurrencyAmount_from_json(requester, obj["channel_total_balance"])
        if obj["channel_total_balance"]
        else None,
        status=parse_enum_optional(ChannelStatus, obj["channel_status"]),
        estimated_force_closure_wait_minutes=obj[
            "channel_estimated_force_closure_wait_minutes"
        ],
        commit_fee=CurrencyAmount_from_json(requester, obj["channel_commit_fee"])
        if obj["channel_commit_fee"]
        else None,
        fees=ChannelFees_from_json(requester, obj["channel_fees"])
        if obj["channel_fees"]
        else None,
        remote_node_id=obj["channel_remote_node"]["id"]
        if obj["channel_remote_node"]
        else None,
        local_node_id=obj["channel_local_node"]["id"],
        short_channel_id=obj["channel_short_channel_id"],
    )
