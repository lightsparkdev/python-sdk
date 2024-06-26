# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.utils.enums import parse_optional_list_of_enums

from .TransactionStatus import TransactionStatus


@dataclass
class OutgoingPaymentsForPaymentHashQueryInput:
    payment_hash: str
    """The 32-byte hash of the payment preimage for which to fetch payments"""

    statuses: Optional[List[TransactionStatus]]
    """An optional filter to only query outgoing payments of given statuses."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "outgoing_payments_for_payment_hash_query_input_payment_hash": self.payment_hash,
            "outgoing_payments_for_payment_hash_query_input_statuses": (
                [e.value for e in self.statuses] if self.statuses else None
            ),
        }


def from_json(obj: Mapping[str, Any]) -> OutgoingPaymentsForPaymentHashQueryInput:
    return OutgoingPaymentsForPaymentHashQueryInput(
        payment_hash=obj["outgoing_payments_for_payment_hash_query_input_payment_hash"],
        statuses=parse_optional_list_of_enums(
            TransactionStatus,
            obj["outgoing_payments_for_payment_hash_query_input_statuses"],
        ),
    )
