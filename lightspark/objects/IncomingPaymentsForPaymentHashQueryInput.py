# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.utils.enums import parse_optional_list_of_enums

from .TransactionStatus import TransactionStatus


@dataclass
class IncomingPaymentsForPaymentHashQueryInput:

    payment_hash: str
    """The 32-byte hash of the payment preimage for which to fetch payments"""

    statuses: Optional[List[TransactionStatus]]
    """An optional filter to only query incoming payments of given statuses."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "incoming_payments_for_payment_hash_query_input_payment_hash": self.payment_hash,
            "incoming_payments_for_payment_hash_query_input_statuses": (
                [e.value for e in self.statuses] if self.statuses else None
            ),
        }


def from_json(obj: Mapping[str, Any]) -> IncomingPaymentsForPaymentHashQueryInput:
    return IncomingPaymentsForPaymentHashQueryInput(
        payment_hash=obj["incoming_payments_for_payment_hash_query_input_payment_hash"],
        statuses=parse_optional_list_of_enums(
            TransactionStatus,
            obj["incoming_payments_for_payment_hash_query_input_statuses"],
        ),
    )
