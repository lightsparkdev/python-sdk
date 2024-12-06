# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester


@dataclass
class InvoiceForPaymentHashOutput:

    requester: Requester

    invoice_id: Optional[str]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "invoice_for_payment_hash_output_invoice": (
                {"id": self.invoice_id} if self.invoice_id else None
            ),
        }


FRAGMENT = """
fragment InvoiceForPaymentHashOutputFragment on InvoiceForPaymentHashOutput {
    __typename
    invoice_for_payment_hash_output_invoice: invoice {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> InvoiceForPaymentHashOutput:
    return InvoiceForPaymentHashOutput(
        requester=requester,
        invoice_id=(
            obj["invoice_for_payment_hash_output_invoice"]["id"]
            if obj["invoice_for_payment_hash_output_invoice"]
            else None
        ),
    )
