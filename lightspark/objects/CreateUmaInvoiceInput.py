# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class CreateUmaInvoiceInput:

    node_id: str

    amount_msats: int

    metadata_hash: str

    expiry_secs: Optional[int]

    receiver_hash: Optional[str]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_uma_invoice_input_node_id": self.node_id,
            "create_uma_invoice_input_amount_msats": self.amount_msats,
            "create_uma_invoice_input_metadata_hash": self.metadata_hash,
            "create_uma_invoice_input_expiry_secs": self.expiry_secs,
            "create_uma_invoice_input_receiver_hash": self.receiver_hash,
        }


def from_json(obj: Mapping[str, Any]) -> CreateUmaInvoiceInput:
    return CreateUmaInvoiceInput(
        node_id=obj["create_uma_invoice_input_node_id"],
        amount_msats=obj["create_uma_invoice_input_amount_msats"],
        metadata_hash=obj["create_uma_invoice_input_metadata_hash"],
        expiry_secs=obj["create_uma_invoice_input_expiry_secs"],
        receiver_hash=obj["create_uma_invoice_input_receiver_hash"],
    )
