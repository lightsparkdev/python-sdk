# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class LightningFeeEstimateForInvoiceInput:
    node_id: str
    """The node from where you want to send the payment."""

    encoded_payment_request: str
    """The invoice you want to pay (as defined by the BOLT11 standard)."""

    amount_msats: Optional[int]
    """If the invoice does not specify a payment amount, then the amount that you wish to pay, expressed in msats."""


def from_json(obj: Mapping[str, Any]) -> LightningFeeEstimateForInvoiceInput:
    return LightningFeeEstimateForInvoiceInput(
        node_id=obj["lightning_fee_estimate_for_invoice_input_node_id"],
        encoded_payment_request=obj[
            "lightning_fee_estimate_for_invoice_input_encoded_payment_request"
        ],
        amount_msats=obj["lightning_fee_estimate_for_invoice_input_amount_msats"],
    )
