# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class ReleasePaymentPreimageOutput:
    requester: Requester

    invoice_id: str


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
