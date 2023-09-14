# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class CreateUmaInvoiceInput:
    node_id: str

    amount_msats: int

    metadata_hash: str

    expiry_secs: Optional[int]


def from_json(obj: Mapping[str, Any]) -> CreateUmaInvoiceInput:
    return CreateUmaInvoiceInput(
        node_id=obj["create_uma_invoice_input_node_id"],
        amount_msats=obj["create_uma_invoice_input_amount_msats"],
        metadata_hash=obj["create_uma_invoice_input_metadata_hash"],
        expiry_secs=obj["create_uma_invoice_input_expiry_secs"],
    )
