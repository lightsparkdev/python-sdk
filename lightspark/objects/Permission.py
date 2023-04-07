# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class Permission(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    ALL = "ALL"
    MAINNET_VIEW = "MAINNET_VIEW"
    MAINNET_TRANSACT = "MAINNET_TRANSACT"
    MAINNET_MANAGE = "MAINNET_MANAGE"
    TESTNET_VIEW = "TESTNET_VIEW"
    TESTNET_TRANSACT = "TESTNET_TRANSACT"
    TESTNET_MANAGE = "TESTNET_MANAGE"
    REGTEST_VIEW = "REGTEST_VIEW"
    REGTEST_TRANSACT = "REGTEST_TRANSACT"
    REGTEST_MANAGE = "REGTEST_MANAGE"
    USER_VIEW = "USER_VIEW"
    USER_MANAGE = "USER_MANAGE"
    ACCOUNT_VIEW = "ACCOUNT_VIEW"
    ACCOUNT_MANAGE = "ACCOUNT_MANAGE"
