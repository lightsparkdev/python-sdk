# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class RiskRating(Enum):
    """This is an enum of the potential risk ratings related to a transaction made over the Lightning Network. These risk ratings are returned from the CryptoSanctionScreeningProvider."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    HIGH_RISK = "HIGH_RISK"
    LOW_RISK = "LOW_RISK"
    UNKNOWN = "UNKNOWN"
