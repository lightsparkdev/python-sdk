# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester


@dataclass
class OutgoingPaymentForIdempotencyKeyOutput:
    requester: Requester

    payment_id: Optional[str]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "outgoing_payment_for_idempotency_key_output_payment": {
                "id": self.payment_id
            }
            if self.payment_id
            else None,
        }


FRAGMENT = """
fragment OutgoingPaymentForIdempotencyKeyOutputFragment on OutgoingPaymentForIdempotencyKeyOutput {
    __typename
    outgoing_payment_for_idempotency_key_output_payment: payment {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> OutgoingPaymentForIdempotencyKeyOutput:
    return OutgoingPaymentForIdempotencyKeyOutput(
        requester=requester,
        payment_id=obj["outgoing_payment_for_idempotency_key_output_payment"]["id"]
        if obj["outgoing_payment_for_idempotency_key_output_payment"]
        else None,
    )
