# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .OutgoingPayment import OutgoingPayment
from .OutgoingPayment import from_json as OutgoingPayment_from_json


@dataclass
class OutgoingPaymentsForPaymentHashQueryOutput:
    requester: Requester

    payments: List[OutgoingPayment]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "outgoing_payments_for_payment_hash_query_output_payments": [
                e.to_json() for e in self.payments
            ],
        }


FRAGMENT = """
fragment OutgoingPaymentsForPaymentHashQueryOutputFragment on OutgoingPaymentsForPaymentHashQueryOutput {
    __typename
    outgoing_payments_for_payment_hash_query_output_payments: payments {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> OutgoingPaymentsForPaymentHashQueryOutput:
    return OutgoingPaymentsForPaymentHashQueryOutput(
        requester=requester,
        payments=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: OutgoingPayment_from_json(requester, e),
                obj["outgoing_payments_for_payment_hash_query_output_payments"],
            )
        ),
    )
