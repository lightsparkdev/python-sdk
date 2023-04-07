# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .IncomingPaymentAttempt import IncomingPaymentAttempt
from .IncomingPaymentAttempt import from_json as IncomingPaymentAttempt_from_json


@dataclass
class IncomingPaymentToAttemptsConnection:
    """The connection from incoming payment to all attempts."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[IncomingPaymentAttempt]
    """The incoming payment attempts for the current page of this connection."""


FRAGMENT = """
fragment IncomingPaymentToAttemptsConnectionFragment on IncomingPaymentToAttemptsConnection {
    __typename
    incoming_payment_to_attempts_connection_count: count
    incoming_payment_to_attempts_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> IncomingPaymentToAttemptsConnection:
    return IncomingPaymentToAttemptsConnection(
        requester=requester,
        count=obj["incoming_payment_to_attempts_connection_count"],
        entities=list(
            map(
                lambda e: IncomingPaymentAttempt_from_json(requester, e),
                obj["incoming_payment_to_attempts_connection_entities"],
            )
        ),
    )
