# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.objects.PaymentFailureReason import PaymentFailureReason
from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .LightningTransaction import LightningTransaction
from .OutgoingPaymentToAttemptsConnection import OutgoingPaymentToAttemptsConnection
from .OutgoingPaymentToAttemptsConnection import (
    from_json as OutgoingPaymentToAttemptsConnection_from_json,
)
from .PaymentFailureReason import PaymentFailureReason
from .PaymentRequestData import PaymentRequestData
from .PaymentRequestData import from_json as PaymentRequestData_from_json
from .RichText import RichText
from .RichText import from_json as RichText_from_json
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class OutgoingPayment(LightningTransaction, Transaction, Entity):
    """A transaction that was sent from a Lightspark node on the Lightning Network."""

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

    origin_id: str
    """The Lightspark node this payment originated from."""

    destination_id: Optional[str]
    """If known, the final recipient node this payment was sent to."""

    fees: Optional[CurrencyAmount]
    """The fees paid by the sender node to send the payment."""

    payment_request_data: Optional[PaymentRequestData]
    """The data of the payment request that was paid by this transaction, if known."""

    failure_reason: Optional[PaymentFailureReason]
    """If applicable, the reason why the payment failed."""

    failure_message: Optional[RichText]
    """If applicable, user-facing error message describing why the payment failed."""
    typename: str

    def get_attempts(
        self, first: Optional[int] = None
    ) -> OutgoingPaymentToAttemptsConnection:
        json = self.requester.execute_graphql(
            """
query FetchOutgoingPaymentToAttemptsConnection($entity_id: ID!, $first: Int) {
    entity(id: $entity_id) {
        ... on OutgoingPayment {
            attempts(, first: $first) {
                __typename
                outgoing_payment_to_attempts_connection_count: count
                outgoing_payment_to_attempts_connection_entities: entities {
                    __typename
                    outgoing_payment_attempt_id: id
                    outgoing_payment_attempt_created_at: created_at
                    outgoing_payment_attempt_updated_at: updated_at
                    outgoing_payment_attempt_status: status
                    outgoing_payment_attempt_failure_code: failure_code
                    outgoing_payment_attempt_failure_source_index: failure_source_index
                    outgoing_payment_attempt_resolved_at: resolved_at
                    outgoing_payment_attempt_amount: amount {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    outgoing_payment_attempt_fees: fees {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    outgoing_payment_attempt_outgoing_payment: outgoing_payment {
                        id
                    }
                }
            }
        }
    }
}
            """,
            {"entity_id": self.id, "first": first},
        )
        connection = json["entity"]["attempts"]
        return OutgoingPaymentToAttemptsConnection_from_json(self.requester, connection)


FRAGMENT = """
fragment OutgoingPaymentFragment on OutgoingPayment {
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
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> OutgoingPayment:
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
