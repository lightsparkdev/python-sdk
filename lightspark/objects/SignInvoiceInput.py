# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class SignInvoiceInput:
    invoice_id: str
    """The unique identifier of the invoice to be signed."""

    signature: str
    """The cryptographic signature for the invoice."""

    recovery_id: int
    """The recovery identifier for the signature."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "sign_invoice_input_invoice_id": self.invoice_id,
            "sign_invoice_input_signature": self.signature,
            "sign_invoice_input_recovery_id": self.recovery_id,
        }


def from_json(obj: Mapping[str, Any]) -> SignInvoiceInput:
    return SignInvoiceInput(
        invoice_id=obj["sign_invoice_input_invoice_id"],
        signature=obj["sign_invoice_input_signature"],
        recovery_id=obj["sign_invoice_input_recovery_id"],
    )
