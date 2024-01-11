# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class CancelInvoiceInput:
    """The unique identifier of the Invoice that should be cancelled. The invoice is supposed to be open, not settled and not expired."""

    invoice_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "cancel_invoice_input_invoice_id": self.invoice_id,
        }


def from_json(obj: Mapping[str, Any]) -> CancelInvoiceInput:
    return CancelInvoiceInput(
        invoice_id=obj["cancel_invoice_input_invoice_id"],
    )
