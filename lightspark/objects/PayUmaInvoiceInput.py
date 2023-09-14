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


def from_json(obj: Mapping[str, Any]) -> PayUmaInvoiceInput:
    return PayUmaInvoiceInput(
        node_id=obj["pay_uma_invoice_input_node_id"],
        encoded_invoice=obj["pay_uma_invoice_input_encoded_invoice"],
        timeout_secs=obj["pay_uma_invoice_input_timeout_secs"],
        maximum_fees_msats=obj["pay_uma_invoice_input_maximum_fees_msats"],
        amount_msats=obj["pay_uma_invoice_input_amount_msats"],
    )
