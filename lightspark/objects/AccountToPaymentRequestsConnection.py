# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester

from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json
from .PaymentRequest import PaymentRequest
from .PaymentRequest import from_json as PaymentRequest_from_json


@dataclass
class AccountToPaymentRequestsConnection:
    requester: Requester

    count: Optional[int]
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[PaymentRequest]
    """The payment requests for the current page of this connection."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""


FRAGMENT = """
fragment AccountToPaymentRequestsConnectionFragment on AccountToPaymentRequestsConnection {
    __typename
    account_to_payment_requests_connection_count: count
    account_to_payment_requests_connection_entities: entities {
        id
    }
    account_to_payment_requests_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> AccountToPaymentRequestsConnection:
    return AccountToPaymentRequestsConnection(
        requester=requester,
        count=obj["account_to_payment_requests_connection_count"],
        entities=list(
            map(
                lambda e: PaymentRequest_from_json(requester, e),
                obj["account_to_payment_requests_connection_entities"],
            )
        ),
        page_info=PageInfo_from_json(
            requester, obj["account_to_payment_requests_connection_page_info"]
        ),
    )
