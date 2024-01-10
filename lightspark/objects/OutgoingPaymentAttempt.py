# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.objects.HtlcAttemptFailureCode import HtlcAttemptFailureCode
from lightspark.objects.OutgoingPaymentAttemptStatus import OutgoingPaymentAttemptStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .HtlcAttemptFailureCode import HtlcAttemptFailureCode
from .OutgoingPaymentAttemptStatus import OutgoingPaymentAttemptStatus
from .OutgoingPaymentAttemptToHopsConnection import (
    OutgoingPaymentAttemptToHopsConnection,
)
from .OutgoingPaymentAttemptToHopsConnection import (
    from_json as OutgoingPaymentAttemptToHopsConnection_from_json,
)


@dataclass
class OutgoingPaymentAttempt(Entity):
    """This object represents an attempted Lightning Network payment sent from a Lightspark Node. You can retrieve this object to receive payment related information about any payment attempt sent from your Lightspark Node on the Lightning Network, including any potential reasons the payment may have failed."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    status: OutgoingPaymentAttemptStatus
    """The status of an outgoing payment attempt."""

    failure_code: Optional[HtlcAttemptFailureCode]
    """If the payment attempt failed, then this contains the Bolt #4 failure code."""

    failure_source_index: Optional[int]
    """If the payment attempt failed, then this contains the index of the hop at which the problem occurred."""

    attempted_at: datetime
    """The date and time when the attempt was initiated."""

    resolved_at: Optional[datetime]
    """The time the outgoing payment attempt failed or succeeded."""

    amount: Optional[CurrencyAmount]
    """The total amount of funds required to complete a payment over this route. This value includes the cumulative fees for each hop. As a result, the attempt extended to the first-hop in the route will need to have at least this much value, otherwise the route will fail at an intermediate node due to an insufficient amount."""

    fees: Optional[CurrencyAmount]
    """The sum of the fees paid at each hop within the route of this attempt. In the case of a one-hop payment, this value will be zero as we don't need to pay a fee to ourselves."""

    outgoing_payment_id: str
    """The outgoing payment for this attempt."""

    channel_snapshot_id: Optional[str]
    """The channel snapshot at the time the outgoing payment attempt was made."""
    typename: str

    def get_hops(
        self, first: Optional[int] = None, after: Optional[str] = None
    ) -> OutgoingPaymentAttemptToHopsConnection:
        json = self.requester.execute_graphql(
            """
query FetchOutgoingPaymentAttemptToHopsConnection($entity_id: ID!, $first: Int, $after: String) {
    entity(id: $entity_id) {
        ... on OutgoingPaymentAttempt {
            hops(, first: $first, after: $after) {
                __typename
                outgoing_payment_attempt_to_hops_connection_count: count
                outgoing_payment_attempt_to_hops_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                outgoing_payment_attempt_to_hops_connection_entities: entities {
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
            }
        }
    }
}
            """,
            {"entity_id": self.id, "first": first, "after": after},
        )
        connection = json["entity"]["hops"]
        return OutgoingPaymentAttemptToHopsConnection_from_json(
            self.requester, connection
        )

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "OutgoingPaymentAttempt",
            "outgoing_payment_attempt_id": self.id,
            "outgoing_payment_attempt_created_at": self.created_at.isoformat(),
            "outgoing_payment_attempt_updated_at": self.updated_at.isoformat(),
            "outgoing_payment_attempt_status": self.status.value,
            "outgoing_payment_attempt_failure_code": self.failure_code.value
            if self.failure_code
            else None,
            "outgoing_payment_attempt_failure_source_index": self.failure_source_index,
            "outgoing_payment_attempt_attempted_at": self.attempted_at.isoformat(),
            "outgoing_payment_attempt_resolved_at": self.resolved_at.isoformat()
            if self.resolved_at
            else None,
            "outgoing_payment_attempt_amount": self.amount.to_json()
            if self.amount
            else None,
            "outgoing_payment_attempt_fees": self.fees.to_json() if self.fees else None,
            "outgoing_payment_attempt_outgoing_payment": {
                "id": self.outgoing_payment_id
            },
            "outgoing_payment_attempt_channel_snapshot": {
                "id": self.channel_snapshot_id
            }
            if self.channel_snapshot_id
            else None,
        }


FRAGMENT = """
fragment OutgoingPaymentAttemptFragment on OutgoingPaymentAttempt {
    __typename
    outgoing_payment_attempt_id: id
    outgoing_payment_attempt_created_at: created_at
    outgoing_payment_attempt_updated_at: updated_at
    outgoing_payment_attempt_status: status
    outgoing_payment_attempt_failure_code: failure_code
    outgoing_payment_attempt_failure_source_index: failure_source_index
    outgoing_payment_attempt_attempted_at: attempted_at
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
    outgoing_payment_attempt_channel_snapshot: channel_snapshot {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> OutgoingPaymentAttempt:
    return OutgoingPaymentAttempt(
        requester=requester,
        typename="OutgoingPaymentAttempt",
        id=obj["outgoing_payment_attempt_id"],
        created_at=datetime.fromisoformat(obj["outgoing_payment_attempt_created_at"]),
        updated_at=datetime.fromisoformat(obj["outgoing_payment_attempt_updated_at"]),
        status=parse_enum(
            OutgoingPaymentAttemptStatus, obj["outgoing_payment_attempt_status"]
        ),
        failure_code=parse_enum_optional(
            HtlcAttemptFailureCode, obj["outgoing_payment_attempt_failure_code"]
        ),
        failure_source_index=obj["outgoing_payment_attempt_failure_source_index"],
        attempted_at=datetime.fromisoformat(
            obj["outgoing_payment_attempt_attempted_at"]
        ),
        resolved_at=datetime.fromisoformat(obj["outgoing_payment_attempt_resolved_at"])
        if obj["outgoing_payment_attempt_resolved_at"]
        else None,
        amount=CurrencyAmount_from_json(
            requester, obj["outgoing_payment_attempt_amount"]
        )
        if obj["outgoing_payment_attempt_amount"]
        else None,
        fees=CurrencyAmount_from_json(requester, obj["outgoing_payment_attempt_fees"])
        if obj["outgoing_payment_attempt_fees"]
        else None,
        outgoing_payment_id=obj["outgoing_payment_attempt_outgoing_payment"]["id"],
        channel_snapshot_id=obj["outgoing_payment_attempt_channel_snapshot"]["id"]
        if obj["outgoing_payment_attempt_channel_snapshot"]
        else None,
    )
