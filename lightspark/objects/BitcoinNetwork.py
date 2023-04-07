# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class BitcoinNetwork(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    MAINNET = "MAINNET"
    """The production version of the Bitcoin Blockchain."""
    REGTEST = "REGTEST"
    """A test version of the Bitcoin Blockchain, maintained by Lightspark."""
    SIGNET = "SIGNET"
    """A test version of the Bitcoin Blockchain, maintained by a centralized organization. Not in use at Lightspark."""
    TESTNET = "TESTNET"
    """A test version of the Bitcoin Blockchain, publically available."""
