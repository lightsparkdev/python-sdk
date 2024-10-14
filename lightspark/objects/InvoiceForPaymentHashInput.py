# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class InvoiceForPaymentHashInput:

    payment_hash: str
    """The 32-byte hash of the payment preimage for which to fetch an invoice."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "invoice_for_payment_hash_input_payment_hash": self.payment_hash,
        }


def from_json(obj: Mapping[str, Any]) -> InvoiceForPaymentHashInput:
    return InvoiceForPaymentHashInput(
        payment_hash=obj["invoice_for_payment_hash_input_payment_hash"],
    )
