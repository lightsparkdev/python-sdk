# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.utils.enums import parse_enum_optional

from .PaymentFailureReason import PaymentFailureReason


@dataclass
class PayTestModeInvoiceInput:

    node_id: str
    """The node from where you want to send the payment."""

    encoded_invoice: str
    """The invoice you want to pay (as defined by the BOLT11 standard)."""

    timeout_secs: int
    """The timeout in seconds that we will try to make the payment."""

    maximum_fees_msats: int
    """The maximum amount of fees that you want to pay for this payment to be sent, expressed in msats."""

    failure_reason: Optional[PaymentFailureReason]
    """The failure reason to trigger for the payment. If not set, pay_invoice will be called."""

    amount_msats: Optional[int]
    """The amount you will pay for this invoice, expressed in msats. It should ONLY be set when the invoice amount is zero."""

    idempotency_key: Optional[str]
    """The idempotency key of the request. The same result will be returned for the same idempotency key."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "pay_test_mode_invoice_input_node_id": self.node_id,
            "pay_test_mode_invoice_input_encoded_invoice": self.encoded_invoice,
            "pay_test_mode_invoice_input_timeout_secs": self.timeout_secs,
            "pay_test_mode_invoice_input_maximum_fees_msats": self.maximum_fees_msats,
            "pay_test_mode_invoice_input_failure_reason": (
                self.failure_reason.value if self.failure_reason else None
            ),
            "pay_test_mode_invoice_input_amount_msats": self.amount_msats,
            "pay_test_mode_invoice_input_idempotency_key": self.idempotency_key,
        }


def from_json(obj: Mapping[str, Any]) -> PayTestModeInvoiceInput:
    return PayTestModeInvoiceInput(
        node_id=obj["pay_test_mode_invoice_input_node_id"],
        encoded_invoice=obj["pay_test_mode_invoice_input_encoded_invoice"],
        timeout_secs=obj["pay_test_mode_invoice_input_timeout_secs"],
        maximum_fees_msats=obj["pay_test_mode_invoice_input_maximum_fees_msats"],
        failure_reason=parse_enum_optional(
            PaymentFailureReason, obj["pay_test_mode_invoice_input_failure_reason"]
        ),
        amount_msats=obj["pay_test_mode_invoice_input_amount_msats"],
        idempotency_key=obj["pay_test_mode_invoice_input_idempotency_key"],
    )
