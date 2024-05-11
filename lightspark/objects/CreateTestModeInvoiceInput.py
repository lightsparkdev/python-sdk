# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.utils.enums import parse_enum_optional

from .InvoiceType import InvoiceType


@dataclass
class CreateTestModeInvoiceInput:
    local_node_id: str

    amount_msats: int

    memo: Optional[str]

    invoice_type: Optional[InvoiceType]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_test_mode_invoice_input_local_node_id": self.local_node_id,
            "create_test_mode_invoice_input_amount_msats": self.amount_msats,
            "create_test_mode_invoice_input_memo": self.memo,
            "create_test_mode_invoice_input_invoice_type": self.invoice_type.value
            if self.invoice_type
            else None,
        }


def from_json(obj: Mapping[str, Any]) -> CreateTestModeInvoiceInput:
    return CreateTestModeInvoiceInput(
        local_node_id=obj["create_test_mode_invoice_input_local_node_id"],
        amount_msats=obj["create_test_mode_invoice_input_amount_msats"],
        memo=obj["create_test_mode_invoice_input_memo"],
        invoice_type=parse_enum_optional(
            InvoiceType, obj["create_test_mode_invoice_input_invoice_type"]
        ),
    )
