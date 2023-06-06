# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateTestModeInvoiceOutput:
    requester: Requester

    encoded_payment_request: str


FRAGMENT = """
fragment CreateTestModeInvoiceOutputFragment on CreateTestModeInvoiceOutput {
    __typename
    create_test_mode_invoice_output_encoded_payment_request: encoded_payment_request
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateTestModeInvoiceOutput:
    return CreateTestModeInvoiceOutput(
        requester=requester,
        encoded_payment_request=obj[
            "create_test_mode_invoice_output_encoded_payment_request"
        ],
    )
