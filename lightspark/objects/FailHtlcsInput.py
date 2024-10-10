# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class FailHtlcsInput:
    invoice_id: str
    """The id of invoice which the pending HTLCs that need to be failed are paying for."""

    cancel_invoice: bool
    """Whether the invoice needs to be canceled after failing the htlcs. If yes, the invoice cannot be paid anymore."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "fail_htlcs_input_invoice_id": self.invoice_id,
            "fail_htlcs_input_cancel_invoice": self.cancel_invoice,
        }


def from_json(obj: Mapping[str, Any]) -> FailHtlcsInput:
    return FailHtlcsInput(
        invoice_id=obj["fail_htlcs_input_invoice_id"],
        cancel_invoice=obj["fail_htlcs_input_cancel_invoice"],
    )
