# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class PayInvoiceOutput:
    requester: Requester

    payment_id: str
    """The payment that has been sent."""


FRAGMENT = """
fragment PayInvoiceOutputFragment on PayInvoiceOutput {
    __typename
    pay_invoice_output_payment: payment {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> PayInvoiceOutput:
    return PayInvoiceOutput(
        requester=requester,
        payment_id=obj["pay_invoice_output_payment"]["id"],
    )
