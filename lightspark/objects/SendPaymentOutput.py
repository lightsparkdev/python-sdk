# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class SendPaymentOutput:
    requester: Requester

    payment_id: str
    """The payment that has been sent."""


FRAGMENT = """
fragment SendPaymentOutputFragment on SendPaymentOutput {
    __typename
    send_payment_output_payment: payment {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> SendPaymentOutput:
    return SendPaymentOutput(
        requester=requester,
        payment_id=obj["send_payment_output_payment"]["id"],
    )
