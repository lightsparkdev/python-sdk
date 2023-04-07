# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class CurrencyUnit(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    BITCOIN = "BITCOIN"
    """Bitcoin is the cryptocurrency native to the Bitcoin network. It is used as the native medium for value transfer for the Lightning Network."""
    SATOSHI = "SATOSHI"
    """0.00000001 (10e-8) Bitcoin or one hundred millionth of a Bitcoin. This is the unit most commonly used in Lightning transactions."""
    MILLISATOSHI = "MILLISATOSHI"
    """0.001 Satoshi, or 10e-11 Bitcoin. We recommend using the Satoshi unit instead when possible."""
    USD = "USD"
    """United States Dollar."""
    NANOBITCOIN = "NANOBITCOIN"
    """0.000000001 (10e-9) Bitcoin or a billionth of a Bitcoin. We recommend using the Satoshi unit instead when possible."""
    MICROBITCOIN = "MICROBITCOIN"
    """0.000001 (10e-6) Bitcoin or a millionth of a Bitcoin. We recommend using the Satoshi unit instead when possible."""
    MILLIBITCOIN = "MILLIBITCOIN"
    """0.001 (10e-3) Bitcoin or a thousandth of a Bitcoin. We recommend using the Satoshi unit instead when possible."""
