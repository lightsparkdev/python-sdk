# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.objects.LightsparkNodePurpose import LightsparkNodePurpose
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_optional

from .LightsparkNode import LightsparkNode
from .LightsparkNode import from_json as LightsparkNode_from_json
from .LightsparkNodePurpose import LightsparkNodePurpose
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json


@dataclass
class AccountToNodesConnection:
    """A connection between an account and the nodes it manages."""

    requester: Requester

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    purpose: Optional[LightsparkNodePurpose]
    """The main purpose for the selected set of nodes. It is automatically determined from the nodes that are selected in this connection and is used for optimization purposes, as well as to determine the variation of the UI that should be presented to the user."""

    entities: List[LightsparkNode]
    """The nodes for the current page of this connection."""


FRAGMENT = """
fragment AccountToNodesConnectionFragment on AccountToNodesConnection {
    __typename
    account_to_nodes_connection_page_info: page_info {
        __typename
        page_info_has_next_page: has_next_page
        page_info_has_previous_page: has_previous_page
        page_info_start_cursor: start_cursor
        page_info_end_cursor: end_cursor
    }
    account_to_nodes_connection_count: count
    account_to_nodes_connection_purpose: purpose
    account_to_nodes_connection_entities: entities {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> AccountToNodesConnection:
    return AccountToNodesConnection(
        requester=requester,
        page_info=PageInfo_from_json(
            requester, obj["account_to_nodes_connection_page_info"]
        ),
        count=obj["account_to_nodes_connection_count"],
        purpose=parse_enum_optional(
            LightsparkNodePurpose, obj["account_to_nodes_connection_purpose"]
        ),
        entities=list(
            map(
                lambda e: LightsparkNode_from_json(requester, e),
                obj["account_to_nodes_connection_entities"],
            )
        ),
    )
