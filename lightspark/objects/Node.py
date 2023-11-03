# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.exceptions import LightsparkException
from lightspark.objects.BitcoinNetwork import BitcoinNetwork
from lightspark.objects.LightsparkNodeStatus import LightsparkNodeStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .Balances import from_json as Balances_from_json
from .BitcoinNetwork import BitcoinNetwork
from .BlockchainBalance import from_json as BlockchainBalance_from_json
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .NodeAddressType import NodeAddressType
from .NodeToAddressesConnection import NodeToAddressesConnection
from .NodeToAddressesConnection import from_json as NodeToAddressesConnection_from_json
from .Secret import from_json as Secret_from_json


@dataclass
class Node(Entity):
    """This object is an interface representing a Lightning Node on the Lightning Network, and could either be a Lightspark node or a node managed by a third party."""

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
    typename: str

    def get_addresses(
        self, first: Optional[int] = None, types: Optional[List[NodeAddressType]] = None
    ) -> NodeToAddressesConnection:
        json = self.requester.execute_graphql(
            """
query FetchNodeToAddressesConnection($entity_id: ID!, $first: Int, $types: [NodeAddressType!]) {
    entity(id: $entity_id) {
        ... on Node {
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


FRAGMENT = """
fragment NodeFragment on Node {
    __typename
    ... on GraphNode {
        __typename
        graph_node_id: id
        graph_node_created_at: created_at
        graph_node_updated_at: updated_at
        graph_node_alias: alias
        graph_node_bitcoin_network: bitcoin_network
        graph_node_color: color
        graph_node_conductivity: conductivity
        graph_node_display_name: display_name
        graph_node_public_key: public_key
    }
    ... on LightsparkNodeWithOSK {
        __typename
        lightspark_node_with_o_s_k_id: id
        lightspark_node_with_o_s_k_created_at: created_at
        lightspark_node_with_o_s_k_updated_at: updated_at
        lightspark_node_with_o_s_k_alias: alias
        lightspark_node_with_o_s_k_bitcoin_network: bitcoin_network
        lightspark_node_with_o_s_k_color: color
        lightspark_node_with_o_s_k_conductivity: conductivity
        lightspark_node_with_o_s_k_display_name: display_name
        lightspark_node_with_o_s_k_public_key: public_key
        lightspark_node_with_o_s_k_owner: owner {
            id
        }
        lightspark_node_with_o_s_k_status: status
        lightspark_node_with_o_s_k_total_balance: total_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        lightspark_node_with_o_s_k_total_local_balance: total_local_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        lightspark_node_with_o_s_k_local_balance: local_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        lightspark_node_with_o_s_k_remote_balance: remote_balance {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        lightspark_node_with_o_s_k_blockchain_balance: blockchain_balance {
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
        lightspark_node_with_o_s_k_uma_prescreening_utxos: uma_prescreening_utxos
        lightspark_node_with_o_s_k_balances: balances {
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
        lightspark_node_with_o_s_k_encrypted_signing_private_key: encrypted_signing_private_key {
            __typename
            secret_encrypted_value: encrypted_value
            secret_cipher: cipher
        }
    }
    ... on LightsparkNodeWithRemoteSigning {
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
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Node:
    if obj["__typename"] == "GraphNode":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.GraphNode import GraphNode

        return GraphNode(
            requester=requester,
            typename="GraphNode",
            id=obj["graph_node_id"],
            created_at=datetime.fromisoformat(obj["graph_node_created_at"]),
            updated_at=datetime.fromisoformat(obj["graph_node_updated_at"]),
            alias=obj["graph_node_alias"],
            bitcoin_network=parse_enum(
                BitcoinNetwork, obj["graph_node_bitcoin_network"]
            ),
            color=obj["graph_node_color"],
            conductivity=obj["graph_node_conductivity"],
            display_name=obj["graph_node_display_name"],
            public_key=obj["graph_node_public_key"],
        )
    if obj["__typename"] == "LightsparkNodeWithOSK":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.LightsparkNodeWithOSK import LightsparkNodeWithOSK

        return LightsparkNodeWithOSK(
            requester=requester,
            typename="LightsparkNodeWithOSK",
            id=obj["lightspark_node_with_o_s_k_id"],
            created_at=datetime.fromisoformat(
                obj["lightspark_node_with_o_s_k_created_at"]
            ),
            updated_at=datetime.fromisoformat(
                obj["lightspark_node_with_o_s_k_updated_at"]
            ),
            alias=obj["lightspark_node_with_o_s_k_alias"],
            bitcoin_network=parse_enum(
                BitcoinNetwork, obj["lightspark_node_with_o_s_k_bitcoin_network"]
            ),
            color=obj["lightspark_node_with_o_s_k_color"],
            conductivity=obj["lightspark_node_with_o_s_k_conductivity"],
            display_name=obj["lightspark_node_with_o_s_k_display_name"],
            public_key=obj["lightspark_node_with_o_s_k_public_key"],
            owner_id=obj["lightspark_node_with_o_s_k_owner"]["id"],
            status=parse_enum_optional(
                LightsparkNodeStatus, obj["lightspark_node_with_o_s_k_status"]
            ),
            total_balance=CurrencyAmount_from_json(
                requester, obj["lightspark_node_with_o_s_k_total_balance"]
            )
            if obj["lightspark_node_with_o_s_k_total_balance"]
            else None,
            total_local_balance=CurrencyAmount_from_json(
                requester, obj["lightspark_node_with_o_s_k_total_local_balance"]
            )
            if obj["lightspark_node_with_o_s_k_total_local_balance"]
            else None,
            local_balance=CurrencyAmount_from_json(
                requester, obj["lightspark_node_with_o_s_k_local_balance"]
            )
            if obj["lightspark_node_with_o_s_k_local_balance"]
            else None,
            remote_balance=CurrencyAmount_from_json(
                requester, obj["lightspark_node_with_o_s_k_remote_balance"]
            )
            if obj["lightspark_node_with_o_s_k_remote_balance"]
            else None,
            blockchain_balance=BlockchainBalance_from_json(
                requester, obj["lightspark_node_with_o_s_k_blockchain_balance"]
            )
            if obj["lightspark_node_with_o_s_k_blockchain_balance"]
            else None,
            uma_prescreening_utxos=obj[
                "lightspark_node_with_o_s_k_uma_prescreening_utxos"
            ],
            balances=Balances_from_json(
                requester, obj["lightspark_node_with_o_s_k_balances"]
            )
            if obj["lightspark_node_with_o_s_k_balances"]
            else None,
            encrypted_signing_private_key=Secret_from_json(
                requester,
                obj["lightspark_node_with_o_s_k_encrypted_signing_private_key"],
            )
            if obj["lightspark_node_with_o_s_k_encrypted_signing_private_key"]
            else None,
        )
    if obj["__typename"] == "LightsparkNodeWithRemoteSigning":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.LightsparkNodeWithRemoteSigning import (
            LightsparkNodeWithRemoteSigning,
        )

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
                BitcoinNetwork,
                obj["lightspark_node_with_remote_signing_bitcoin_network"],
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
                requester,
                obj["lightspark_node_with_remote_signing_total_local_balance"],
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
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface Node corresponding to the typename={graphql_typename}",
    )
