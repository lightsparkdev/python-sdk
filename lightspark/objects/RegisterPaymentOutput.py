# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class RegisterPaymentOutput:
    requester: Requester

    payment_id: str


FRAGMENT = """
fragment RegisterPaymentOutputFragment on RegisterPaymentOutput {
    __typename
    register_payment_output_payment: payment {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> RegisterPaymentOutput:
    return RegisterPaymentOutput(
        requester=requester,
        payment_id=obj["register_payment_output_payment"]["id"],
    )
