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

    incoming_payment_id: str
    """The payment that has been received."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_test_mode_paymentoutput_payment": {"id": self.payment_id},
            "create_test_mode_paymentoutput_incoming_payment": {
                "id": self.incoming_payment_id
            },
        }


FRAGMENT = """
fragment CreateTestModePaymentoutputFragment on CreateTestModePaymentoutput {
    __typename
    create_test_mode_paymentoutput_payment: payment {
        id
    }
    create_test_mode_paymentoutput_incoming_payment: incoming_payment {
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
        incoming_payment_id=obj["create_test_mode_paymentoutput_incoming_payment"][
            "id"
        ],
    )
