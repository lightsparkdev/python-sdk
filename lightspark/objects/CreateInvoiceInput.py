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
    """The expiry of the invoice in seconds. Default value is 86400 (1 day)."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_invoice_input_node_id": self.node_id,
            "create_invoice_input_amount_msats": self.amount_msats,
            "create_invoice_input_memo": self.memo,
            "create_invoice_input_invoice_type": (
                self.invoice_type.value if self.invoice_type else None
            ),
            "create_invoice_input_expiry_secs": self.expiry_secs,
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
    )
