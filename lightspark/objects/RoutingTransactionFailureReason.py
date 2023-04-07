# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class RoutingTransactionFailureReason(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    INCOMING_LINK_FAILURE = "INCOMING_LINK_FAILURE"
    OUTGOING_LINK_FAILURE = "OUTGOING_LINK_FAILURE"
    FORWARDING_FAILURE = "FORWARDING_FAILURE"
