# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .OutgoingPaymentAttempt import OutgoingPaymentAttempt
from .OutgoingPaymentAttempt import from_json as OutgoingPaymentAttempt_from_json


@dataclass
class OutgoingPaymentToAttemptsConnection:
    """The connection from outgoing payment to all attempts."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[OutgoingPaymentAttempt]
    """The attempts for the current page of this connection."""


FRAGMENT = """
fragment OutgoingPaymentToAttemptsConnectionFragment on OutgoingPaymentToAttemptsConnection {
    __typename
    outgoing_payment_to_attempts_connection_count: count
    outgoing_payment_to_attempts_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> OutgoingPaymentToAttemptsConnection:
    return OutgoingPaymentToAttemptsConnection(
        requester=requester,
        count=obj["outgoing_payment_to_attempts_connection_count"],
        entities=list(
            map(
                lambda e: OutgoingPaymentAttempt_from_json(requester, e),
                obj["outgoing_payment_to_attempts_connection_entities"],
            )
        ),
    )
