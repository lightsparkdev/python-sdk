# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Hop import Hop
from .Hop import from_json as Hop_from_json


@dataclass
class OutgoingPaymentAttemptToHopsConnection:
    """The connection from an outgoing payment attempt to the list of sequential hops that define the path from sender node to recipient node."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[Hop]
    """The hops for the current page of this connection."""


FRAGMENT = """
fragment OutgoingPaymentAttemptToHopsConnectionFragment on OutgoingPaymentAttemptToHopsConnection {
    __typename
    outgoing_payment_attempt_to_hops_connection_count: count
    outgoing_payment_attempt_to_hops_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> OutgoingPaymentAttemptToHopsConnection:
    return OutgoingPaymentAttemptToHopsConnection(
        requester=requester,
        count=obj["outgoing_payment_attempt_to_hops_connection_count"],
        entities=list(
            map(
                lambda e: Hop_from_json(requester, e),
                obj["outgoing_payment_attempt_to_hops_connection_entities"],
            )
        ),
    )
