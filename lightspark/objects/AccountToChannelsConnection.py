# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Channel import Channel
from .Channel import from_json as Channel_from_json


@dataclass
class AccountToChannelsConnection:
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[Channel]
    """The channels for the current page of this connection."""


FRAGMENT = """
fragment AccountToChannelsConnectionFragment on AccountToChannelsConnection {
    __typename
    account_to_channels_connection_count: count
    account_to_channels_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> AccountToChannelsConnection:
    return AccountToChannelsConnection(
        requester=requester,
        count=obj["account_to_channels_connection_count"],
        entities=list(
            map(
                lambda e: Channel_from_json(requester, e),
                obj["account_to_channels_connection_entities"],
            )
        ),
    )
