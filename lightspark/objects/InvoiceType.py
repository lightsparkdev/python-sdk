# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class InvoiceType(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    STANDARD = "STANDARD"
    """A standard Bolt 11 invoice."""
    AMP = "AMP"
    """An AMP (Atomic Multi-path Payment) invoice."""
