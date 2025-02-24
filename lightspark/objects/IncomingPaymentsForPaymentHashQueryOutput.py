# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .IncomingPayment import IncomingPayment
from .IncomingPayment import from_json as IncomingPayment_from_json


@dataclass
class IncomingPaymentsForPaymentHashQueryOutput:

    requester: Requester

    payments: List[IncomingPayment]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "incoming_payments_for_payment_hash_query_output_payments": [
                e.to_json() for e in self.payments
            ],
        }


FRAGMENT = """
fragment IncomingPaymentsForPaymentHashQueryOutputFragment on IncomingPaymentsForPaymentHashQueryOutput {
    __typename
    incoming_payments_for_payment_hash_query_output_payments: payments {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> IncomingPaymentsForPaymentHashQueryOutput:
    return IncomingPaymentsForPaymentHashQueryOutput(
        requester=requester,
        payments=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: IncomingPayment_from_json(requester, e),
                obj["incoming_payments_for_payment_hash_query_output_payments"],
            )
        ),
    )
