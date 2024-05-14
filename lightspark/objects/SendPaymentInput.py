# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class SendPaymentInput:
    node_id: str
    """The node from where you want to send the payment."""

    destination_public_key: str
    """The public key of the destination node."""

    timeout_secs: int
    """The timeout in seconds that we will try to make the payment."""

    amount_msats: int
    """The amount you will send to the destination node, expressed in msats."""

    maximum_fees_msats: int
    """The maximum amount of fees that you want to pay for this payment to be sent, expressed in msats."""

    idempotency_key: Optional[str]
    """The idempotency key of the request. The same result will be returned for the same idempotency key."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "send_payment_input_node_id": self.node_id,
            "send_payment_input_destination_public_key": self.destination_public_key,
            "send_payment_input_timeout_secs": self.timeout_secs,
            "send_payment_input_amount_msats": self.amount_msats,
            "send_payment_input_maximum_fees_msats": self.maximum_fees_msats,
            "send_payment_input_idempotency_key": self.idempotency_key,
        }


def from_json(obj: Mapping[str, Any]) -> SendPaymentInput:
    return SendPaymentInput(
        node_id=obj["send_payment_input_node_id"],
        destination_public_key=obj["send_payment_input_destination_public_key"],
        timeout_secs=obj["send_payment_input_timeout_secs"],
        amount_msats=obj["send_payment_input_amount_msats"],
        maximum_fees_msats=obj["send_payment_input_maximum_fees_msats"],
        idempotency_key=obj["send_payment_input_idempotency_key"],
    )
