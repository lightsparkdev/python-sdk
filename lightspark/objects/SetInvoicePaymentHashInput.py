# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class SetInvoicePaymentHashInput:
    invoice_id: str
    """The invoice that needs to be updated."""

    payment_hash: str
    """The 32-byte hash of the payment preimage."""

    preimage_nonce: str
    """The 32-byte nonce used to generate the invoice preimage."""


def from_json(obj: Mapping[str, Any]) -> SetInvoicePaymentHashInput:
    return SetInvoicePaymentHashInput(
        invoice_id=obj["set_invoice_payment_hash_input_invoice_id"],
        payment_hash=obj["set_invoice_payment_hash_input_payment_hash"],
        preimage_nonce=obj["set_invoice_payment_hash_input_preimage_nonce"],
    )
