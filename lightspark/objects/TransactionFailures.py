# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.utils.enums import parse_optional_list_of_enums

from .PaymentFailureReason import PaymentFailureReason
from .RoutingTransactionFailureReason import RoutingTransactionFailureReason


@dataclass
class TransactionFailures:
    payment_failures: Optional[List[PaymentFailureReason]]

    routing_transaction_failures: Optional[List[RoutingTransactionFailureReason]]


def from_json(obj: Mapping[str, Any]) -> TransactionFailures:
    return TransactionFailures(
        payment_failures=parse_optional_list_of_enums(
            PaymentFailureReason, obj["transaction_failures_payment_failures"]
        ),
        routing_transaction_failures=parse_optional_list_of_enums(
            RoutingTransactionFailureReason,
            obj["transaction_failures_routing_transaction_failures"],
        ),
    )
