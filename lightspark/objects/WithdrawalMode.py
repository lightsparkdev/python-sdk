
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class WithdrawalMode(Enum):
    """This is an enum of the potential modes that your Bitcoin withdrawal can take."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    WALLET_ONLY = "WALLET_ONLY"
    WALLET_THEN_CHANNELS = "WALLET_THEN_CHANNELS"

