# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .Balances import Balances
from .Balances import from_json as Balances_from_json
from .BitcoinNetwork import BitcoinNetwork
from .BlockchainBalance import BlockchainBalance
from .BlockchainBalance import from_json as BlockchainBalance_from_json
from .ChannelStatus import ChannelStatus
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .LightningPaymentDirection import LightningPaymentDirection
from .LightsparkNode import LightsparkNode
from .LightsparkNodeStatus import LightsparkNodeStatus
from .LightsparkNodeToChannelsConnection import LightsparkNodeToChannelsConnection
from .LightsparkNodeToChannelsConnection import (
    from_json as LightsparkNodeToChannelsConnection_from_json,
)
from .LightsparkNodeToDailyLiquidityForecastsConnection import (
    LightsparkNodeToDailyLiquidityForecastsConnection,
)
from .LightsparkNodeToDailyLiquidityForecastsConnection import (
    from_json as LightsparkNodeToDailyLiquidityForecastsConnection_from_json,
)
from .Node import Node
from .NodeAddressType import NodeAddressType
from .NodeToAddressesConnection import NodeToAddressesConnection
from .NodeToAddressesConnection import from_json as NodeToAddressesConnection_from_json


@dataclass
class LightsparkNodeWithRemoteSigning(LightsparkNode, Node, Entity):
    """This is a Lightspark node with remote signing."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    alias: Optional[str]
    """A name that identifies the node. It has no importance in terms of operating the node, it is just a way to identify and search for commercial services or popular nodes. This alias can be changed at any time by the node operator."""

    bitcoin_network: BitcoinNetwork
    """The Bitcoin Network this node is deployed in."""

    color: Optional[str]
    """A hexadecimal string that describes a color. For example "#000000" is black, "#FFFFFF" is white. It has no importance in terms of operating the node, it is just a way to visually differentiate nodes. That color can be changed at any time by the node operator."""

    conductivity: Optional[int]
    """A summary metric used to capture how well positioned a node is to send, receive, or route transactions efficiently. Maximizing a node's conductivity helps a node’s transactions to be capital efficient. The value is an integer ranging between 0 and 10 (bounds included)."""

    display_name: str
    """The name of this node in the network. It will be the most human-readable option possible, depending on the data available for this node."""

    public_key: Optional[str]
    """The public key of this node. It acts as a unique identifier of this node in the Lightning Network."""

    owner_id: str
    """The owner of this LightsparkNode."""

    status: Optional[LightsparkNodeStatus]
    """The current status of this node."""

    total_balance: Optional[CurrencyAmount]
    """The sum of the balance on the Bitcoin Network, channel balances, and commit fees on this node."""

    total_local_balance: Optional[CurrencyAmount]
    """The total sum of the channel balances (online and offline) on this node."""

    local_balance: Optional[CurrencyAmount]
    """The sum of the channel balances (online only) that are available to send on this node."""

    remote_balance: Optional[CurrencyAmount]
    """The sum of the channel balances that are available to receive on this node."""

    blockchain_balance: Optional[BlockchainBalance]
    """The details of the balance of this node on the Bitcoin Network."""

    uma_prescreening_utxos: List[str]
    """The utxos of the channels that are connected to this node. This is used in uma flow for pre-screening."""

    balances: Optional[Balances]
    """The balances that describe the funds in this node."""
    typename: str

    def get_addresses(
        self, first: Optional[int] = None, types: Optional[List[NodeAddressType]] = None
    ) -> NodeToAddressesConnection:
        json = self.requester.execute_graphql(
            """
query FetchNodeToAddressesConnection($entity_id: ID!, $first: Int, $types: [NodeAddressType!]) {
    entity(id: $entity_id) {
        ... on LightsparkNodeWithRemoteSigning {
            addresses(, first: $first, types: $types) {
                __typename
                node_to_addresses_connection_count: count
                node_to_addresses_connection_entities: entities {
                    __typename
                    node_address_address: address
                    node_address_type: type
                }
            }
        }
    }
}
            """,
            {"entity_id": self.id, "first": first, "types": types},
        )
        connection = json["entity"]["addresses"]
        return NodeToAddressesConnection_from_json(self.requester, connection)

    def get_channels(
        self,
        first: Optional[int] = None,
        statuses: Optional[List[ChannelStatus]] = None,
        after: Optional[str] = None,
    ) -> LightsparkNodeToChannelsConnection:
        json = self.requester.execute_graphql(
            """
query FetchLightsparkNodeToChannelsConnection($entity_id: ID!, $first: Int, $statuses: [ChannelStatus!], $after: String) {
    entity(id: $entity_id) {
        ... on LightsparkNodeWithRemoteSigning {
            channels(, first: $first, statuses: $statuses, after: $after) {
                __typename
                lightspark_node_to_channels_connection_count: count
                lightspark_node_to_channels_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                lightspark_node_to_channels_connection_entities: entities {
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
            }
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "first": first,
                "statuses": statuses,
                "after": after,
            },
        )
        connection = json["entity"]["channels"]
        return LightsparkNodeToChannelsConnection_from_json(self.requester, connection)

    def get_daily_liquidity_forecasts(
        self,
        from_date: datetime,
        to_date: datetime,
        direction: LightningPaymentDirection,
    ) -> LightsparkNodeToDailyLiquidityForecastsConnection:
        json = self.requester.execute_graphql(
            """
query FetchLightsparkNodeToDailyLiquidityForecastsConnection($entity_id: ID!, $from_date: Date!, $to_date: Date!, $direction: LightningPaymentDirection!) {
    entity(id: $entity_id) {
        ... on LightsparkNodeWithRemoteSigning {
            daily_liquidity_forecasts(, from_date: $from_date, to_date: $to_date, direction: $direction) {
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
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "from_date": from_date,
                "to_date": to_date,
                "direction": direction,
            },
        )
        connection = json["entity"]["daily_liquidity_forecasts"]
        return LightsparkNodeToDailyLiquidityForecastsConnection_from_json(
            self.requester, connection
        )

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "LightsparkNodeWithRemoteSigning",
            "lightspark_node_with_remote_signing_id": self.id,
            "lightspark_node_with_remote_signing_created_at": self.created_at.isoformat(),
            "lightspark_node_with_remote_signing_updated_at": self.updated_at.isoformat(),
            "lightspark_node_with_remote_signing_alias": self.alias,
            "lightspark_node_with_remote_signing_bitcoin_network": self.bitcoin_network.value,
            "lightspark_node_with_remote_signing_color": self.color,
            "lightspark_node_with_remote_signing_conductivity": self.conductivity,
            "lightspark_node_with_remote_signing_display_name": self.display_name,
            "lightspark_node_with_remote_signing_public_key": self.public_key,
            "lightspark_node_with_remote_signing_owner": {"id": self.owner_id},
            "lightspark_node_with_remote_signing_status": self.status.value
            if self.status
            else None,
            "lightspark_node_with_remote_signing_total_balance": self.total_balance.to_json()
            if self.total_balance
            else None,
            "lightspark_node_with_remote_signing_total_local_balance": self.total_local_balance.to_json()
            if self.total_local_balance
            else None,
            "lightspark_node_with_remote_signing_local_balance": self.local_balance.to_json()
            if self.local_balance
            else None,
            "lightspark_node_with_remote_signing_remote_balance": self.remote_balance.to_json()
            if self.remote_balance
            else None,
            "lightspark_node_with_remote_signing_blockchain_balance": self.blockchain_balance.to_json()
            if self.blockchain_balance
            else None,
            "lightspark_node_with_remote_signing_uma_prescreening_utxos": self.uma_prescreening_utxos,
            "lightspark_node_with_remote_signing_balances": self.balances.to_json()
            if self.balances
            else None,
        }


FRAGMENT = """
fragment LightsparkNodeWithRemoteSigningFragment on LightsparkNodeWithRemoteSigning {
    __typename
    lightspark_node_with_remote_signing_id: id
    lightspark_node_with_remote_signing_created_at: created_at
    lightspark_node_with_remote_signing_updated_at: updated_at
    lightspark_node_with_remote_signing_alias: alias
    lightspark_node_with_remote_signing_bitcoin_network: bitcoin_network
    lightspark_node_with_remote_signing_color: color
    lightspark_node_with_remote_signing_conductivity: conductivity
    lightspark_node_with_remote_signing_display_name: display_name
    lightspark_node_with_remote_signing_public_key: public_key
    lightspark_node_with_remote_signing_owner: owner {
        id
    }
    lightspark_node_with_remote_signing_status: status
    lightspark_node_with_remote_signing_total_balance: total_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    lightspark_node_with_remote_signing_total_local_balance: total_local_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    lightspark_node_with_remote_signing_local_balance: local_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    lightspark_node_with_remote_signing_remote_balance: remote_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    lightspark_node_with_remote_signing_blockchain_balance: blockchain_balance {
        __typename
        blockchain_balance_total_balance: total_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        blockchain_balance_confirmed_balance: confirmed_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        blockchain_balance_unconfirmed_balance: unconfirmed_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        blockchain_balance_locked_balance: locked_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        blockchain_balance_required_reserve: required_reserve {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        blockchain_balance_available_balance: available_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
    }
    lightspark_node_with_remote_signing_uma_prescreening_utxos: uma_prescreening_utxos
    lightspark_node_with_remote_signing_balances: balances {
        __typename
        balances_owned_balance: owned_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        balances_available_to_send_balance: available_to_send_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        balances_available_to_withdraw_balance: available_to_withdraw_balance {
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
) -> LightsparkNodeWithRemoteSigning:
    return LightsparkNodeWithRemoteSigning(
        requester=requester,
        typename="LightsparkNodeWithRemoteSigning",
        id=obj["lightspark_node_with_remote_signing_id"],
        created_at=datetime.fromisoformat(
            obj["lightspark_node_with_remote_signing_created_at"]
        ),
        updated_at=datetime.fromisoformat(
            obj["lightspark_node_with_remote_signing_updated_at"]
        ),
        alias=obj["lightspark_node_with_remote_signing_alias"],
        bitcoin_network=parse_enum(
            BitcoinNetwork, obj["lightspark_node_with_remote_signing_bitcoin_network"]
        ),
        color=obj["lightspark_node_with_remote_signing_color"],
        conductivity=obj["lightspark_node_with_remote_signing_conductivity"],
        display_name=obj["lightspark_node_with_remote_signing_display_name"],
        public_key=obj["lightspark_node_with_remote_signing_public_key"],
        owner_id=obj["lightspark_node_with_remote_signing_owner"]["id"],
        status=parse_enum_optional(
            LightsparkNodeStatus, obj["lightspark_node_with_remote_signing_status"]
        ),
        total_balance=CurrencyAmount_from_json(
            requester, obj["lightspark_node_with_remote_signing_total_balance"]
        )
        if obj["lightspark_node_with_remote_signing_total_balance"]
        else None,
        total_local_balance=CurrencyAmount_from_json(
            requester, obj["lightspark_node_with_remote_signing_total_local_balance"]
        )
        if obj["lightspark_node_with_remote_signing_total_local_balance"]
        else None,
        local_balance=CurrencyAmount_from_json(
            requester, obj["lightspark_node_with_remote_signing_local_balance"]
        )
        if obj["lightspark_node_with_remote_signing_local_balance"]
        else None,
        remote_balance=CurrencyAmount_from_json(
            requester, obj["lightspark_node_with_remote_signing_remote_balance"]
        )
        if obj["lightspark_node_with_remote_signing_remote_balance"]
        else None,
        blockchain_balance=BlockchainBalance_from_json(
            requester, obj["lightspark_node_with_remote_signing_blockchain_balance"]
        )
        if obj["lightspark_node_with_remote_signing_blockchain_balance"]
        else None,
        uma_prescreening_utxos=obj[
            "lightspark_node_with_remote_signing_uma_prescreening_utxos"
        ],
        balances=Balances_from_json(
            requester, obj["lightspark_node_with_remote_signing_balances"]
        )
        if obj["lightspark_node_with_remote_signing_balances"]
        else None,
    )
