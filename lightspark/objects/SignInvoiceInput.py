# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class SignInvoiceInput:
    invoice_id: str

    signature: str

    recovery_id: int


def from_json(obj: Mapping[str, Any]) -> SignInvoiceInput:
    return SignInvoiceInput(
        invoice_id=obj["sign_invoice_input_invoice_id"],
        signature=obj["sign_invoice_input_signature"],
        recovery_id=obj["sign_invoice_input_recovery_id"],
    )
