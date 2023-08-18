# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateTestModePaymentoutput:
    """This is an object identifying the output of a test mode payment. This object can be used to retrieve the associated payment made from a Test Mode Payment call."""

    requester: Requester

    payment_id: str
    """The payment that has been sent."""


FRAGMENT = """
fragment CreateTestModePaymentoutputFragment on CreateTestModePaymentoutput {
    __typename
    create_test_mode_paymentoutput_payment: payment {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateTestModePaymentoutput:
    return CreateTestModePaymentoutput(
        requester=requester,
        payment_id=obj["create_test_mode_paymentoutput_payment"]["id"],
    )
