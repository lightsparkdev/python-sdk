# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class PayUmaInvoiceInput:
    node_id: str

    encoded_invoice: str

    timeout_secs: int

    maximum_fees_msats: int

    amount_msats: Optional[int]

    idempotency_key: Optional[str]

    sender_hash: Optional[str]
    """An optional, monthly-rotated, unique hashed identifier corresponding to the sender of the payment."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "pay_uma_invoice_input_node_id": self.node_id,
            "pay_uma_invoice_input_encoded_invoice": self.encoded_invoice,
            "pay_uma_invoice_input_timeout_secs": self.timeout_secs,
            "pay_uma_invoice_input_maximum_fees_msats": self.maximum_fees_msats,
            "pay_uma_invoice_input_amount_msats": self.amount_msats,
            "pay_uma_invoice_input_idempotency_key": self.idempotency_key,
            "pay_uma_invoice_input_sender_hash": self.sender_hash,
        }


def from_json(obj: Mapping[str, Any]) -> PayUmaInvoiceInput:
    return PayUmaInvoiceInput(
        node_id=obj["pay_uma_invoice_input_node_id"],
        encoded_invoice=obj["pay_uma_invoice_input_encoded_invoice"],
        timeout_secs=obj["pay_uma_invoice_input_timeout_secs"],
        maximum_fees_msats=obj["pay_uma_invoice_input_maximum_fees_msats"],
        amount_msats=obj["pay_uma_invoice_input_amount_msats"],
        idempotency_key=obj["pay_uma_invoice_input_idempotency_key"],
        sender_hash=obj["pay_uma_invoice_input_sender_hash"],
    )
