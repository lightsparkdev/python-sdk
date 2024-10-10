# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class SignInvoiceOutput:
    requester: Requester

    invoice_id: str
    """ The signed invoice object."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "sign_invoice_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment SignInvoiceOutputFragment on SignInvoiceOutput {
    __typename
    sign_invoice_output_invoice: invoice {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> SignInvoiceOutput:
    return SignInvoiceOutput(
        requester=requester,
        invoice_id=obj["sign_invoice_output_invoice"]["id"],
    )
