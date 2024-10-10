# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .ChannelClosingTransaction import ChannelClosingTransaction
from .ChannelClosingTransaction import from_json as ChannelClosingTransaction_from_json
from .Connection import Connection
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class WithdrawalRequestToChannelClosingTransactionsConnection(Connection):
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    entities: List[ChannelClosingTransaction]
    """The channel closing transactions for the current page of this connection."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "WithdrawalRequestToChannelClosingTransactionsConnection",
            "withdrawal_request_to_channel_closing_transactions_connection_count": self.count,
            "withdrawal_request_to_channel_closing_transactions_connection_page_info": self.page_info.to_json(),
            "withdrawal_request_to_channel_closing_transactions_connection_entities": [
                e.to_json() for e in self.entities
            ],
        }


FRAGMENT = """
fragment WithdrawalRequestToChannelClosingTransactionsConnectionFragment on WithdrawalRequestToChannelClosingTransactionsConnection {
    __typename
    withdrawal_request_to_channel_closing_transactions_connection_count: count
    withdrawal_request_to_channel_closing_transactions_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
    withdrawal_request_to_channel_closing_transactions_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> WithdrawalRequestToChannelClosingTransactionsConnection:
    return WithdrawalRequestToChannelClosingTransactionsConnection(
        requester=requester,
        typename="WithdrawalRequestToChannelClosingTransactionsConnection",
        count=obj[
            "withdrawal_request_to_channel_closing_transactions_connection_count"
        ],
        page_info=PageInfo_from_json(
            requester,
            obj[
                "withdrawal_request_to_channel_closing_transactions_connection_page_info"
            ],
        ),
        entities=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: ChannelClosingTransaction_from_json(requester, e),
                obj[
                    "withdrawal_request_to_channel_closing_transactions_connection_entities"
                ],
            )
        ),
    )
