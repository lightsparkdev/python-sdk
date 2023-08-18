# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Connection import Connection
from .IncomingPaymentAttempt import IncomingPaymentAttempt
from .IncomingPaymentAttempt import from_json as IncomingPaymentAttempt_from_json
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class IncomingPaymentToAttemptsConnection(Connection):
    """The connection from incoming payment to all attempts."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    entities: List[IncomingPaymentAttempt]
    """The incoming payment attempts for the current page of this connection."""
    typename: str


FRAGMENT = """
fragment IncomingPaymentToAttemptsConnectionFragment on IncomingPaymentToAttemptsConnection {
    __typename
    incoming_payment_to_attempts_connection_count: count
    incoming_payment_to_attempts_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
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
        typename="IncomingPaymentToAttemptsConnection",
        count=obj["incoming_payment_to_attempts_connection_count"],
        page_info=PageInfo_from_json(
            requester, obj["incoming_payment_to_attempts_connection_page_info"]
        ),
        entities=list(
            map(
                lambda e: IncomingPaymentAttempt_from_json(requester, e),
                obj["incoming_payment_to_attempts_connection_entities"],
            )
        ),
    )
