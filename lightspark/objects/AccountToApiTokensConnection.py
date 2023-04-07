# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .ApiToken import ApiToken
from .ApiToken import from_json as ApiToken_from_json
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class AccountToApiTokensConnection:
    requester: Requester

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[ApiToken]
    """The API tokens for the current page of this connection."""


FRAGMENT = """
fragment AccountToApiTokensConnectionFragment on AccountToApiTokensConnection {
    __typename
    account_to_api_tokens_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
    account_to_api_tokens_connection_count: count
    account_to_api_tokens_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> AccountToApiTokensConnection:
    return AccountToApiTokensConnection(
        requester=requester,
        page_info=PageInfo_from_json(
            requester, obj["account_to_api_tokens_connection_page_info"]
        ),
        count=obj["account_to_api_tokens_connection_count"],
        entities=list(
            map(
                lambda e: ApiToken_from_json(requester, e),
                obj["account_to_api_tokens_connection_entities"],
            )
        ),
    )
