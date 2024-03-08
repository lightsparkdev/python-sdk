# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .IncomingPaymentAttemptStatus import IncomingPaymentAttemptStatus
from .IncomingPaymentToAttemptsConnection import IncomingPaymentToAttemptsConnection
from .IncomingPaymentToAttemptsConnection import (
    from_json as IncomingPaymentToAttemptsConnection_from_json,
)
from .LightningTransaction import LightningTransaction
from .PostTransactionData import PostTransactionData
from .PostTransactionData import from_json as PostTransactionData_from_json
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class IncomingPayment(LightningTransaction, Transaction, Entity):
    """This object represents any payment sent to a Lightspark node on the Lightning Network. You can retrieve this object to receive payment related information about a specific payment received by a Lightspark node."""

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

    is_uma: bool
    """Whether this payment is an UMA payment or not. NOTE: this field is only set if the invoice that is being paid has been created using the recommended `create_uma_invoice` function."""

    destination_id: str
    """The recipient Lightspark node this payment was sent to."""

    payment_request_id: Optional[str]
    """The optional payment request for this incoming payment, which will be null if the payment is sent through keysend."""

    uma_post_transaction_data: Optional[List[PostTransactionData]]
    """The post transaction data which can be used in KYT payment registration."""

    is_internal_payment: bool
    """Whether the payment is made from the same node."""
    typename: str

    def get_attempts(
        self,
        first: Optional[int] = None,
        statuses: Optional[List[IncomingPaymentAttemptStatus]] = None,
        after: Optional[str] = None,
    ) -> IncomingPaymentToAttemptsConnection:
        json = self.requester.execute_graphql(
            """
query FetchIncomingPaymentToAttemptsConnection($entity_id: ID!, $first: Int, $statuses: [IncomingPaymentAttemptStatus!], $after: String) {
    entity(id: $entity_id) {
        ... on IncomingPayment {
            attempts(, first: $first, statuses: $statuses, after: $after) {
                __typename
                incoming_payment_to_attempts_connection_count: count
                incoming_payment_to_attempts_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                incoming_payment_to_attempts_connection_entities: entities {
                    __typename
                    incoming_payment_attempt_id: id
                    incoming_payment_attempt_created_at: created_at
                    incoming_payment_attempt_updated_at: updated_at
                    incoming_payment_attempt_status: status
                    incoming_payment_attempt_resolved_at: resolved_at
                    incoming_payment_attempt_amount: amount {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    incoming_payment_attempt_channel: channel {
                        id
                    }
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
        connection = json["entity"]["attempts"]
        return IncomingPaymentToAttemptsConnection_from_json(self.requester, connection)

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "IncomingPayment",
            "incoming_payment_id": self.id,
            "incoming_payment_created_at": self.created_at.isoformat(),
            "incoming_payment_updated_at": self.updated_at.isoformat(),
            "incoming_payment_status": self.status.value,
            "incoming_payment_resolved_at": self.resolved_at.isoformat()
            if self.resolved_at
            else None,
            "incoming_payment_amount": self.amount.to_json(),
            "incoming_payment_transaction_hash": self.transaction_hash,
            "incoming_payment_is_uma": self.is_uma,
            "incoming_payment_destination": {"id": self.destination_id},
            "incoming_payment_payment_request": {"id": self.payment_request_id}
            if self.payment_request_id
            else None,
            "incoming_payment_uma_post_transaction_data": [
                e.to_json() for e in self.uma_post_transaction_data
            ]
            if self.uma_post_transaction_data
            else None,
            "incoming_payment_is_internal_payment": self.is_internal_payment,
        }


FRAGMENT = """
fragment IncomingPaymentFragment on IncomingPayment {
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
    incoming_payment_is_uma: is_uma
    incoming_payment_destination: destination {
        id
    }
    incoming_payment_payment_request: payment_request {
        id
    }
    incoming_payment_uma_post_transaction_data: uma_post_transaction_data {
        __typename
        post_transaction_data_utxo: utxo
        post_transaction_data_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
    }
    incoming_payment_is_internal_payment: is_internal_payment
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> IncomingPayment:
    return IncomingPayment(
        requester=requester,
        typename="IncomingPayment",
        id=obj["incoming_payment_id"],
        created_at=datetime.fromisoformat(obj["incoming_payment_created_at"]),
        updated_at=datetime.fromisoformat(obj["incoming_payment_updated_at"]),
        status=parse_enum(TransactionStatus, obj["incoming_payment_status"]),
        resolved_at=datetime.fromisoformat(obj["incoming_payment_resolved_at"])
        if obj["incoming_payment_resolved_at"]
        else None,
        amount=CurrencyAmount_from_json(requester, obj["incoming_payment_amount"]),
        transaction_hash=obj["incoming_payment_transaction_hash"],
        is_uma=obj["incoming_payment_is_uma"],
        destination_id=obj["incoming_payment_destination"]["id"],
        payment_request_id=obj["incoming_payment_payment_request"]["id"]
        if obj["incoming_payment_payment_request"]
        else None,
        uma_post_transaction_data=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: PostTransactionData_from_json(requester, e),
                obj["incoming_payment_uma_post_transaction_data"],
            )
        )
        if obj["incoming_payment_uma_post_transaction_data"]
        else None,
        is_internal_payment=obj["incoming_payment_is_internal_payment"],
    )
