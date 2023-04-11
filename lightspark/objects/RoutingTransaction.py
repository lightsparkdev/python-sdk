# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.objects.RoutingTransactionFailureReason import (
    RoutingTransactionFailureReason,
)
from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .LightningTransaction import LightningTransaction
from .RichText import RichText
from .RichText import from_json as RichText_from_json
from .RoutingTransactionFailureReason import RoutingTransactionFailureReason
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class RoutingTransaction(LightningTransaction, Transaction, Entity):
    """A transaction that was forwarded through a Lightspark node on the Lightning Network."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when this transaction was initiated."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    status: TransactionStatus
    """The current status of this transaction."""

    resolved_at: Optional[datetime]
    """The date and time when this transaction was completed or failed."""

    amount: CurrencyAmount
    """The amount of money involved in this transaction."""

    transaction_hash: Optional[str]
    """The hash of this transaction, so it can be uniquely identified on the Lightning Network."""

    incoming_channel_id: Optional[str]
    """If known, the channel this transaction was received from."""

    outgoing_channel_id: Optional[str]
    """If known, the channel this transaction was forwarded to."""

    fees: Optional[CurrencyAmount]
    """The fees collected by the node when routing this transaction. We subtract the outgoing amount to the incoming amount to determine how much fees were collected."""

    failure_message: Optional[RichText]
    """If applicable, user-facing error message describing why the routing failed."""

    failure_reason: Optional[RoutingTransactionFailureReason]
    """If applicable, the reason why the routing failed."""
    typename: str


FRAGMENT = """
fragment RoutingTransactionFragment on RoutingTransaction {
    __typename
    routing_transaction_id: id
    routing_transaction_created_at: created_at
    routing_transaction_updated_at: updated_at
    routing_transaction_status: status
    routing_transaction_resolved_at: resolved_at
    routing_transaction_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    routing_transaction_transaction_hash: transaction_hash
    routing_transaction_incoming_channel: incoming_channel {
        id
    }
    routing_transaction_outgoing_channel: outgoing_channel {
        id
    }
    routing_transaction_fees: fees {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    routing_transaction_failure_message: failure_message {
        __typename
        rich_text_text: text
    }
    routing_transaction_failure_reason: failure_reason
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> RoutingTransaction:
    return RoutingTransaction(
        requester=requester,
        typename="RoutingTransaction",
        id=obj["routing_transaction_id"],
        created_at=obj["routing_transaction_created_at"],
        updated_at=obj["routing_transaction_updated_at"],
        status=parse_enum(TransactionStatus, obj["routing_transaction_status"]),
        resolved_at=obj["routing_transaction_resolved_at"],
        amount=CurrencyAmount_from_json(requester, obj["routing_transaction_amount"]),
        transaction_hash=obj["routing_transaction_transaction_hash"],
        incoming_channel_id=obj["routing_transaction_incoming_channel"]["id"]
        if obj["routing_transaction_incoming_channel"]
        else None,
        outgoing_channel_id=obj["routing_transaction_outgoing_channel"]["id"]
        if obj["routing_transaction_outgoing_channel"]
        else None,
        fees=CurrencyAmount_from_json(requester, obj["routing_transaction_fees"])
        if obj["routing_transaction_fees"]
        else None,
        failure_message=RichText_from_json(
            requester, obj["routing_transaction_failure_message"]
        )
        if obj["routing_transaction_failure_message"]
        else None,
        failure_reason=parse_enum_optional(
            RoutingTransactionFailureReason, obj["routing_transaction_failure_reason"]
        ),
    )
