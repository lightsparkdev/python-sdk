# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class SetInvoicePaymentHashOutput:
    requester: Requester

    invoice_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "set_invoice_payment_hash_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment SetInvoicePaymentHashOutputFragment on SetInvoicePaymentHashOutput {
    __typename
    set_invoice_payment_hash_output_invoice: invoice {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> SetInvoicePaymentHashOutput:
    return SetInvoicePaymentHashOutput(
        requester=requester,
        invoice_id=obj["set_invoice_payment_hash_output_invoice"]["id"],
    )
