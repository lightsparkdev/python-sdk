# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateInvoiceOutput:

    requester: Requester

    invoice_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_invoice_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment CreateInvoiceOutputFragment on CreateInvoiceOutput {
    __typename
    create_invoice_output_invoice: invoice {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> CreateInvoiceOutput:
    return CreateInvoiceOutput(
        requester=requester,
        invoice_id=obj["create_invoice_output_invoice"]["id"],
    )
