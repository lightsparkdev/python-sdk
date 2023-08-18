# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class NodeAddressType(Enum):
    """This is an enum of the potential types of addresses that a node on the Lightning Network can have."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    TOR = "TOR"
