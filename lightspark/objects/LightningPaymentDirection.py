# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class LightningPaymentDirection(Enum):
    """This is an enum identifying the payment direction."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    INCOMING = "INCOMING"
    """A payment that is received by the node."""
    OUTGOING = "OUTGOING"
    """A payment that is sent by the node."""
