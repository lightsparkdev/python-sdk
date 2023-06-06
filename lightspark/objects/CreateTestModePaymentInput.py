# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class CreateTestModePaymentInput:
    local_node_id: str
    """The node to where you want to send the payment."""

    encoded_invoice: str
    """The invoice you want to be paid (as defined by the BOLT11 standard)."""

    amount_msats: Optional[int]
    """The amount you will be paid for this invoice, expressed in msats. It should ONLY be set when the invoice amount is zero."""


def from_json(obj: Mapping[str, Any]) -> CreateTestModePaymentInput:
    return CreateTestModePaymentInput(
        local_node_id=obj["create_test_mode_payment_input_local_node_id"],
        encoded_invoice=obj["create_test_mode_payment_input_encoded_invoice"],
        amount_msats=obj["create_test_mode_payment_input_amount_msats"],
    )
