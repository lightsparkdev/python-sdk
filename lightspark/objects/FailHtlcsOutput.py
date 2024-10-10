# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class FailHtlcsOutput:
    requester: Requester

    invoice_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "fail_htlcs_output_invoice": {"id": self.invoice_id},
        }


FRAGMENT = """
fragment FailHtlcsOutputFragment on FailHtlcsOutput {
    __typename
    fail_htlcs_output_invoice: invoice {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> FailHtlcsOutput:
    return FailHtlcsOutput(
        requester=requester,
        invoice_id=obj["fail_htlcs_output_invoice"]["id"],
    )
