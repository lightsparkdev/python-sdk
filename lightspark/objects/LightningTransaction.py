# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.exceptions import LightsparkException
from lightspark.objects.PaymentFailureReason import PaymentFailureReason
from lightspark.objects.RoutingTransactionFailureReason import (
    RoutingTransactionFailureReason,
)
from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .PaymentRequestData import from_json as PaymentRequestData_from_json
from .RichText import from_json as RichText_from_json
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class LightningTransaction(Transaction, Entity):
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
    typename: str


FRAGMENT = """
fragment LightningTransactionFragment on LightningTransaction {
    __typename
    ... on IncomingPayment {
        __typename
        incoming_payment_id: id
        incoming_payment_created_at: created_at
        incoming_payment_updated_at: updated_at
        incoming_payment_status: status
        incoming_payment_resolved_at: resolved_at
        incoming_payment_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        incoming_payment_transaction_hash: transaction_hash
        incoming_payment_origin: origin {
            id
        }
        incoming_payment_destination: destination {
            id
        }
        incoming_payment_payment_request: payment_request {
            id
        }
    }
    ... on OutgoingPayment {
        __typename
        outgoing_payment_id: id
        outgoing_payment_created_at: created_at
        outgoing_payment_updated_at: updated_at
        outgoing_payment_status: status
        outgoing_payment_resolved_at: resolved_at
        outgoing_payment_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        outgoing_payment_transaction_hash: transaction_hash
        outgoing_payment_origin: origin {
            id
        }
        outgoing_payment_destination: destination {
            id
        }
        outgoing_payment_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        outgoing_payment_payment_request_data: payment_request_data {
            __typename
            ... on InvoiceData {
                __typename
                invoice_data_encoded_payment_request: encoded_payment_request
                invoice_data_bitcoin_network: bitcoin_network
                invoice_data_payment_hash: payment_hash
                invoice_data_amount: amount {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                invoice_data_created_at: created_at
                invoice_data_expires_at: expires_at
                invoice_data_destination: destination {
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
                    ... on LightsparkNode {
                        __typename
                        lightspark_node_id: id
                        lightspark_node_created_at: created_at
                        lightspark_node_updated_at: updated_at
                        lightspark_node_alias: alias
                        lightspark_node_bitcoin_network: bitcoin_network
                        lightspark_node_color: color
                        lightspark_node_conductivity: conductivity
                        lightspark_node_display_name: display_name
                        lightspark_node_public_key: public_key
                        lightspark_node_account: account {
                            id
                        }
                        lightspark_node_blockchain_balance: blockchain_balance {
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
                        lightspark_node_encrypted_signing_private_key: encrypted_signing_private_key {
                            __typename
                            secret_encrypted_value: encrypted_value
                            secret_cipher: cipher
                        }
                        lightspark_node_total_balance: total_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_total_local_balance: total_local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_local_balance: local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_purpose: purpose
                        lightspark_node_remote_balance: remote_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_status: status
                    }
                }
                invoice_data_memo: memo
            }
        }
        outgoing_payment_failure_reason: failure_reason
        outgoing_payment_failure_message: failure_message {
            __typename
            rich_text_text: text
        }
    }
    ... on RoutingTransaction {
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
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> LightningTransaction:
    if obj["__typename"] == "IncomingPayment":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.IncomingPayment import IncomingPayment

        return IncomingPayment(
            requester=requester,
            typename="IncomingPayment",
            id=obj["incoming_payment_id"],
            created_at=obj["incoming_payment_created_at"],
            updated_at=obj["incoming_payment_updated_at"],
            status=parse_enum(TransactionStatus, obj["incoming_payment_status"]),
            resolved_at=obj["incoming_payment_resolved_at"],
            amount=CurrencyAmount_from_json(requester, obj["incoming_payment_amount"]),
            transaction_hash=obj["incoming_payment_transaction_hash"],
            origin_id=obj["incoming_payment_origin"]["id"]
            if obj["incoming_payment_origin"]
            else None,
            destination_id=obj["incoming_payment_destination"]["id"],
            payment_request_id=obj["incoming_payment_payment_request"]["id"]
            if obj["incoming_payment_payment_request"]
            else None,
        )
    if obj["__typename"] == "OutgoingPayment":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.OutgoingPayment import OutgoingPayment

        return OutgoingPayment(
            requester=requester,
            typename="OutgoingPayment",
            id=obj["outgoing_payment_id"],
            created_at=obj["outgoing_payment_created_at"],
            updated_at=obj["outgoing_payment_updated_at"],
            status=parse_enum(TransactionStatus, obj["outgoing_payment_status"]),
            resolved_at=obj["outgoing_payment_resolved_at"],
            amount=CurrencyAmount_from_json(requester, obj["outgoing_payment_amount"]),
            transaction_hash=obj["outgoing_payment_transaction_hash"],
            origin_id=obj["outgoing_payment_origin"]["id"],
            destination_id=obj["outgoing_payment_destination"]["id"]
            if obj["outgoing_payment_destination"]
            else None,
            fees=CurrencyAmount_from_json(requester, obj["outgoing_payment_fees"])
            if obj["outgoing_payment_fees"]
            else None,
            payment_request_data=PaymentRequestData_from_json(
                requester, obj["outgoing_payment_payment_request_data"]
            )
            if obj["outgoing_payment_payment_request_data"]
            else None,
            failure_reason=parse_enum_optional(
                PaymentFailureReason, obj["outgoing_payment_failure_reason"]
            ),
            failure_message=RichText_from_json(
                requester, obj["outgoing_payment_failure_message"]
            )
            if obj["outgoing_payment_failure_message"]
            else None,
        )
    if obj["__typename"] == "RoutingTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.RoutingTransaction import RoutingTransaction

        return RoutingTransaction(
            requester=requester,
            typename="RoutingTransaction",
            id=obj["routing_transaction_id"],
            created_at=obj["routing_transaction_created_at"],
            updated_at=obj["routing_transaction_updated_at"],
            status=parse_enum(TransactionStatus, obj["routing_transaction_status"]),
            resolved_at=obj["routing_transaction_resolved_at"],
            amount=CurrencyAmount_from_json(
                requester, obj["routing_transaction_amount"]
            ),
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
                RoutingTransactionFailureReason,
                obj["routing_transaction_failure_reason"],
            ),
        )
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface LightningTransaction corresponding to the typename={graphql_typename}",
    )
