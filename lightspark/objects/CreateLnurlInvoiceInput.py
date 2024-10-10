# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class CreateLnurlInvoiceInput:
    node_id: str
    """The node from which to create the invoice."""

    amount_msats: int
    """The amount for which the invoice should be created, in millisatoshis."""

    metadata_hash: str
    """The SHA256 hash of the LNURL metadata payload. This will be present in the h-tag (SHA256 purpose of payment) of the resulting Bolt 11 invoice."""

    expiry_secs: Optional[int]
    """The expiry of the invoice in seconds. Default value is 86400 (1 day)."""

    receiver_hash: Optional[str]
    """An optional, monthly-rotated, unique hashed identifier corresponding to the receiver of the payment."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_lnurl_invoice_input_node_id": self.node_id,
            "create_lnurl_invoice_input_amount_msats": self.amount_msats,
            "create_lnurl_invoice_input_metadata_hash": self.metadata_hash,
            "create_lnurl_invoice_input_expiry_secs": self.expiry_secs,
            "create_lnurl_invoice_input_receiver_hash": self.receiver_hash,
        }


def from_json(obj: Mapping[str, Any]) -> CreateLnurlInvoiceInput:
    return CreateLnurlInvoiceInput(
        node_id=obj["create_lnurl_invoice_input_node_id"],
        amount_msats=obj["create_lnurl_invoice_input_amount_msats"],
        metadata_hash=obj["create_lnurl_invoice_input_metadata_hash"],
        expiry_secs=obj["create_lnurl_invoice_input_expiry_secs"],
        receiver_hash=obj["create_lnurl_invoice_input_receiver_hash"],
    )
