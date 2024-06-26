# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class OnChainFeeTarget(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    HIGH = "HIGH"
    """Transaction expected to be confirmed within 2 blocks."""
    MEDIUM = "MEDIUM"
    """Transaction expected to be confirmed within 6 blocks."""
    LOW = "LOW"
    """Transaction expected to be confirmed within 18 blocks."""
    BACKGROUND = "BACKGROUND"
    """Transaction expected to be confirmed within 50 blocks."""
