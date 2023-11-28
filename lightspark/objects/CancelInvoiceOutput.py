# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CancelInvoiceOutput:
    requester: Requester

    invoice_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "cancel_invoice_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment CancelInvoiceOutputFragment on CancelInvoiceOutput {
    __typename
    cancel_invoice_output_invoice: invoice {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> CancelInvoiceOutput:
    return CancelInvoiceOutput(
        requester=requester,
        invoice_id=obj["cancel_invoice_output_invoice"]["id"],
    )
