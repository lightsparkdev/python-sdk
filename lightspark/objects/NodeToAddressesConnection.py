# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .NodeAddress import NodeAddress
from .NodeAddress import from_json as NodeAddress_from_json


@dataclass
class NodeToAddressesConnection:
    """A connection between a node and the addresses it has announced for itself on Lightning Network."""

    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[NodeAddress]
    """The addresses for the current page of this connection."""


FRAGMENT = """
fragment NodeToAddressesConnectionFragment on NodeToAddressesConnection {
    __typename
    node_to_addresses_connection_count: count
    node_to_addresses_connection_entities: entities {
        __typename
        node_address_address: address
        node_address_type: type
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> NodeToAddressesConnection:
    return NodeToAddressesConnection(
        requester=requester,
        count=obj["node_to_addresses_connection_count"],
        entities=list(
            map(
                lambda e: NodeAddress_from_json(requester, e),
                obj["node_to_addresses_connection_entities"],
            )
        ),
    )
