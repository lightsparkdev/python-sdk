# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity


@dataclass
class Hop(Entity):
    """One hop signifies a payment moving one node ahead on a payment route; a list of sequential hops defines the path from sender node to recipient node for a payment attempt."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    destination_id: Optional[str]
    """The destination node of the hop."""

    index: int
    """The zero-based index position of this hop in the path"""

    public_key: Optional[str]
    """The public key of the node to which the hop is bound."""

    amount_to_forward: Optional[CurrencyAmount]
    """The amount that is to be forwarded to the destination node."""

    fee: Optional[CurrencyAmount]
    """The fees to be collected by the source node for forwarding the payment over the hop."""

    expiry_block_height: Optional[int]
    """The block height at which an unsettled HTLC is considered expired."""
    typename: str


FRAGMENT = """
fragment HopFragment on Hop {
    __typename
    hop_id: id
    hop_created_at: created_at
    hop_updated_at: updated_at
    hop_destination: destination {
        id
    }
    hop_index: index
    hop_public_key: public_key
    hop_amount_to_forward: amount_to_forward {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    hop_fee: fee {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    hop_expiry_block_height: expiry_block_height
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Hop:
    return Hop(
        requester=requester,
        typename="Hop",
        id=obj["hop_id"],
        created_at=obj["hop_created_at"],
        updated_at=obj["hop_updated_at"],
        destination_id=obj["hop_destination"]["id"] if obj["hop_destination"] else None,
        index=obj["hop_index"],
        public_key=obj["hop_public_key"],
        amount_to_forward=CurrencyAmount_from_json(
            requester, obj["hop_amount_to_forward"]
        )
        if obj["hop_amount_to_forward"]
        else None,
        fee=CurrencyAmount_from_json(requester, obj["hop_fee"])
        if obj["hop_fee"]
        else None,
        expiry_block_height=obj["hop_expiry_block_height"],
    )
