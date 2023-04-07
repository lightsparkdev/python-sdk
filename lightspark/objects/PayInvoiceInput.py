# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class PayInvoiceInput:
    node_id: str
    """The node from where you want to send the payment."""

    encoded_invoice: str
    """The invoice you want to pay (as defined by the BOLT11 standard)."""

    timeout_secs: int
    """The timeout in seconds that we will try to make the payment."""

    maximum_fees_msats: int
    """The maximum amount of fees that you want to pay for this payment to be sent, expressed in msats."""

    amount_msats: Optional[int]
    """The amount you will pay for this invoice, expressed in msats. It should ONLY be set when the invoice amount is zero."""


def from_json(obj: Mapping[str, Any]) -> PayInvoiceInput:
    return PayInvoiceInput(
        node_id=obj["pay_invoice_input_node_id"],
        encoded_invoice=obj["pay_invoice_input_encoded_invoice"],
        timeout_secs=obj["pay_invoice_input_timeout_secs"],
        maximum_fees_msats=obj["pay_invoice_input_maximum_fees_msats"],
        amount_msats=obj["pay_invoice_input_amount_msats"],
    )
