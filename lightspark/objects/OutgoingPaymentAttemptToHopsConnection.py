# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Connection import Connection
from .Hop import Hop
from .Hop import from_json as Hop_from_json
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class OutgoingPaymentAttemptToHopsConnection(Connection):
    """The connection from an outgoing payment attempt to the list of sequential hops that define the path from sender node to recipient node."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    entities: List[Hop]
    """The hops for the current page of this connection."""
    typename: str


FRAGMENT = """
fragment OutgoingPaymentAttemptToHopsConnectionFragment on OutgoingPaymentAttemptToHopsConnection {
    __typename
    outgoing_payment_attempt_to_hops_connection_count: count
    outgoing_payment_attempt_to_hops_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
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
        typename="OutgoingPaymentAttemptToHopsConnection",
        count=obj["outgoing_payment_attempt_to_hops_connection_count"],
        page_info=PageInfo_from_json(
            requester, obj["outgoing_payment_attempt_to_hops_connection_page_info"]
        ),
        entities=list(
            map(
                lambda e: Hop_from_json(requester, e),
                obj["outgoing_payment_attempt_to_hops_connection_entities"],
            )
        ),
    )
