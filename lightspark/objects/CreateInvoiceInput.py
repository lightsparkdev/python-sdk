# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.utils.enums import parse_enum_optional

from .InvoiceType import InvoiceType


@dataclass
class CreateInvoiceInput:

    node_id: str
    """The node from which to create the invoice."""

    amount_msats: int
    """The amount for which the invoice should be created, in millisatoshis. Setting the amount to 0 will allow the payer to specify an amount."""

    memo: Optional[str]

    invoice_type: Optional[InvoiceType]

    expiry_secs: Optional[int]
    """The expiry of the invoice in seconds. Default value is 86400 (1 day) for AMP invoice, or 3600 (1 hour) for STANDARD invoice."""

    payment_hash: Optional[str]
    """The payment hash of the invoice. It should only be set if your node is a remote signing node. If not set, it will be requested through REMOTE_SIGNING webhooks with sub event type REQUEST_INVOICE_PAYMENT_HASH."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_invoice_input_node_id": self.node_id,
            "create_invoice_input_amount_msats": self.amount_msats,
            "create_invoice_input_memo": self.memo,
            "create_invoice_input_invoice_type": (
                self.invoice_type.value if self.invoice_type else None
            ),
            "create_invoice_input_expiry_secs": self.expiry_secs,
            "create_invoice_input_payment_hash": self.payment_hash,
        }


def from_json(obj: Mapping[str, Any]) -> CreateInvoiceInput:
    return CreateInvoiceInput(
        node_id=obj["create_invoice_input_node_id"],
        amount_msats=obj["create_invoice_input_amount_msats"],
        memo=obj["create_invoice_input_memo"],
        invoice_type=parse_enum_optional(
            InvoiceType, obj["create_invoice_input_invoice_type"]
        ),
        expiry_secs=obj["create_invoice_input_expiry_secs"],
        payment_hash=obj["create_invoice_input_payment_hash"],
    )
