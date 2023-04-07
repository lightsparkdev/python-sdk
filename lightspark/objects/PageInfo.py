# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester


@dataclass
class PageInfo:
    requester: Requester

    has_next_page: Optional[bool]

    has_previous_page: Optional[bool]

    start_cursor: Optional[str]

    end_cursor: Optional[str]


FRAGMENT = """
fragment PageInfoFragment on PageInfo {
    __typename
    page_info_has_next_page: has_next_page
    page_info_has_previous_page: has_previous_page
    page_info_start_cursor: start_cursor
    page_info_end_cursor: end_cursor
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> PageInfo:
    return PageInfo(
        requester=requester,
        has_next_page=obj["page_info_has_next_page"],
        has_previous_page=obj["page_info_has_previous_page"],
        start_cursor=obj["page_info_start_cursor"],
        end_cursor=obj["page_info_end_cursor"],
    )
