# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.exceptions import LightsparkException
from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class OnChainTransaction(Transaction, Entity):
    """Transaction happened on Bitcoin blockchain."""

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

    fees: Optional[CurrencyAmount]
    """The fees that were paid by the wallet sending the transaction to commit it to the Bitcoin blockchain."""

    block_hash: Optional[str]
    """The hash of the block that included this transaction. This will be null for unconfirmed transactions."""

    block_height: int
    """The height of the block that included this transaction. This will be zero for unconfirmed transactions."""

    destination_addresses: List[str]
    """The Bitcoin blockchain addresses this transaction was sent to."""

    num_confirmations: Optional[int]
    """The number of blockchain confirmations for this transaction in real time."""
    typename: str


FRAGMENT = """
fragment OnChainTransactionFragment on OnChainTransaction {
    __typename
    ... on ChannelClosingTransaction {
        __typename
        channel_closing_transaction_id: id
        channel_closing_transaction_created_at: created_at
        channel_closing_transaction_updated_at: updated_at
        channel_closing_transaction_status: status
        channel_closing_transaction_resolved_at: resolved_at
        channel_closing_transaction_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_closing_transaction_transaction_hash: transaction_hash
        channel_closing_transaction_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_closing_transaction_block_hash: block_hash
        channel_closing_transaction_block_height: block_height
        channel_closing_transaction_destination_addresses: destination_addresses
        channel_closing_transaction_num_confirmations: num_confirmations
        channel_closing_transaction_channel: channel {
            id
        }
    }
    ... on ChannelOpeningTransaction {
        __typename
        channel_opening_transaction_id: id
        channel_opening_transaction_created_at: created_at
        channel_opening_transaction_updated_at: updated_at
        channel_opening_transaction_status: status
        channel_opening_transaction_resolved_at: resolved_at
        channel_opening_transaction_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_opening_transaction_transaction_hash: transaction_hash
        channel_opening_transaction_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_opening_transaction_block_hash: block_hash
        channel_opening_transaction_block_height: block_height
        channel_opening_transaction_destination_addresses: destination_addresses
        channel_opening_transaction_num_confirmations: num_confirmations
        channel_opening_transaction_channel: channel {
            id
        }
    }
    ... on Deposit {
        __typename
        deposit_id: id
        deposit_created_at: created_at
        deposit_updated_at: updated_at
        deposit_status: status
        deposit_resolved_at: resolved_at
        deposit_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        deposit_transaction_hash: transaction_hash
        deposit_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        deposit_block_hash: block_hash
        deposit_block_height: block_height
        deposit_destination_addresses: destination_addresses
        deposit_num_confirmations: num_confirmations
        deposit_destination: destination {
            id
        }
    }
    ... on Withdrawal {
        __typename
        withdrawal_id: id
        withdrawal_created_at: created_at
        withdrawal_updated_at: updated_at
        withdrawal_status: status
        withdrawal_resolved_at: resolved_at
        withdrawal_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        withdrawal_transaction_hash: transaction_hash
        withdrawal_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        withdrawal_block_hash: block_hash
        withdrawal_block_height: block_height
        withdrawal_destination_addresses: destination_addresses
        withdrawal_num_confirmations: num_confirmations
        withdrawal_origin: origin {
            id
        }
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> OnChainTransaction:
    if obj["__typename"] == "ChannelClosingTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.ChannelClosingTransaction import (
            ChannelClosingTransaction,
        )

        return ChannelClosingTransaction(
            requester=requester,
            typename="ChannelClosingTransaction",
            id=obj["channel_closing_transaction_id"],
            created_at=obj["channel_closing_transaction_created_at"],
            updated_at=obj["channel_closing_transaction_updated_at"],
            status=parse_enum(
                TransactionStatus, obj["channel_closing_transaction_status"]
            ),
            resolved_at=obj["channel_closing_transaction_resolved_at"],
            amount=CurrencyAmount_from_json(
                requester, obj["channel_closing_transaction_amount"]
            ),
            transaction_hash=obj["channel_closing_transaction_transaction_hash"],
            fees=CurrencyAmount_from_json(
                requester, obj["channel_closing_transaction_fees"]
            )
            if obj["channel_closing_transaction_fees"]
            else None,
            block_hash=obj["channel_closing_transaction_block_hash"],
            block_height=obj["channel_closing_transaction_block_height"],
            destination_addresses=obj[
                "channel_closing_transaction_destination_addresses"
            ],
            num_confirmations=obj["channel_closing_transaction_num_confirmations"],
            channel_id=obj["channel_closing_transaction_channel"]["id"]
            if obj["channel_closing_transaction_channel"]
            else None,
        )
    if obj["__typename"] == "ChannelOpeningTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.ChannelOpeningTransaction import (
            ChannelOpeningTransaction,
        )

        return ChannelOpeningTransaction(
            requester=requester,
            typename="ChannelOpeningTransaction",
            id=obj["channel_opening_transaction_id"],
            created_at=obj["channel_opening_transaction_created_at"],
            updated_at=obj["channel_opening_transaction_updated_at"],
            status=parse_enum(
                TransactionStatus, obj["channel_opening_transaction_status"]
            ),
            resolved_at=obj["channel_opening_transaction_resolved_at"],
            amount=CurrencyAmount_from_json(
                requester, obj["channel_opening_transaction_amount"]
            ),
            transaction_hash=obj["channel_opening_transaction_transaction_hash"],
            fees=CurrencyAmount_from_json(
                requester, obj["channel_opening_transaction_fees"]
            )
            if obj["channel_opening_transaction_fees"]
            else None,
            block_hash=obj["channel_opening_transaction_block_hash"],
            block_height=obj["channel_opening_transaction_block_height"],
            destination_addresses=obj[
                "channel_opening_transaction_destination_addresses"
            ],
            num_confirmations=obj["channel_opening_transaction_num_confirmations"],
            channel_id=obj["channel_opening_transaction_channel"]["id"]
            if obj["channel_opening_transaction_channel"]
            else None,
        )
    if obj["__typename"] == "Deposit":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Deposit import Deposit

        return Deposit(
            requester=requester,
            typename="Deposit",
            id=obj["deposit_id"],
            created_at=obj["deposit_created_at"],
            updated_at=obj["deposit_updated_at"],
            status=parse_enum(TransactionStatus, obj["deposit_status"]),
            resolved_at=obj["deposit_resolved_at"],
            amount=CurrencyAmount_from_json(requester, obj["deposit_amount"]),
            transaction_hash=obj["deposit_transaction_hash"],
            fees=CurrencyAmount_from_json(requester, obj["deposit_fees"])
            if obj["deposit_fees"]
            else None,
            block_hash=obj["deposit_block_hash"],
            block_height=obj["deposit_block_height"],
            destination_addresses=obj["deposit_destination_addresses"],
            num_confirmations=obj["deposit_num_confirmations"],
            destination_id=obj["deposit_destination"]["id"],
        )
    if obj["__typename"] == "Withdrawal":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Withdrawal import Withdrawal

        return Withdrawal(
            requester=requester,
            typename="Withdrawal",
            id=obj["withdrawal_id"],
            created_at=obj["withdrawal_created_at"],
            updated_at=obj["withdrawal_updated_at"],
            status=parse_enum(TransactionStatus, obj["withdrawal_status"]),
            resolved_at=obj["withdrawal_resolved_at"],
            amount=CurrencyAmount_from_json(requester, obj["withdrawal_amount"]),
            transaction_hash=obj["withdrawal_transaction_hash"],
            fees=CurrencyAmount_from_json(requester, obj["withdrawal_fees"])
            if obj["withdrawal_fees"]
            else None,
            block_hash=obj["withdrawal_block_hash"],
            block_height=obj["withdrawal_block_height"],
            destination_addresses=obj["withdrawal_destination_addresses"],
            num_confirmations=obj["withdrawal_num_confirmations"],
            origin_id=obj["withdrawal_origin"]["id"],
        )
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface OnChainTransaction corresponding to the typename={graphql_typename}",
    )
