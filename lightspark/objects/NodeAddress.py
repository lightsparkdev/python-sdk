# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.NodeAddressType import NodeAddressType
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .NodeAddressType import NodeAddressType


@dataclass
class NodeAddress:
    """An object that represents the address of a node on the Lightning Network."""

    requester: Requester

    address: str
    """The string representation of the address."""

    type: NodeAddressType
    """The type, or protocol, of this address."""


FRAGMENT = """
fragment NodeAddressFragment on NodeAddress {
    __typename
    node_address_address: address
    node_address_type: type
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> NodeAddress:
    return NodeAddress(
        requester=requester,
        address=obj["node_address_address"],
        type=parse_enum(NodeAddressType, obj["node_address_type"]),
    )
