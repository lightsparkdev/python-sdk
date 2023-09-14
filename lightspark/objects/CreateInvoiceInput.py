# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.objects.InvoiceType import InvoiceType
from lightspark.utils.enums import parse_enum_optional

from .InvoiceType import InvoiceType


@dataclass
class CreateInvoiceInput:
    node_id: str
    """The node from which to create the invoice."""

    amount_msats: int
    """The amount for which the invoice should be created, in millisatoshis."""

    memo: Optional[str]

    invoice_type: Optional[InvoiceType]

    expiry_secs: Optional[int]
    """The expiry of the invoice in seconds. Default value is 86400 (1 day)."""


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
