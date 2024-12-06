# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class OutgoingPaymentForIdempotencyKeyInput:

    idempotency_key: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "outgoing_payment_for_idempotency_key_input_idempotency_key": self.idempotency_key,
        }


def from_json(obj: Mapping[str, Any]) -> OutgoingPaymentForIdempotencyKeyInput:
    return OutgoingPaymentForIdempotencyKeyInput(
        idempotency_key=obj[
            "outgoing_payment_for_idempotency_key_input_idempotency_key"
        ],
    )
