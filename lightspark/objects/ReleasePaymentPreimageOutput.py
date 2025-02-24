# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class ReleasePaymentPreimageOutput:

    requester: Requester

    invoice_id: str
    """The invoice of the transaction."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "release_payment_preimage_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment ReleasePaymentPreimageOutputFragment on ReleasePaymentPreimageOutput {
    __typename
    release_payment_preimage_output_invoice: invoice {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ReleasePaymentPreimageOutput:
    return ReleasePaymentPreimageOutput(
        requester=requester,
        invoice_id=obj["release_payment_preimage_output_invoice"]["id"],
    )
