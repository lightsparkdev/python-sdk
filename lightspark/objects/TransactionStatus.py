# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class TransactionStatus(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    SUCCESS = "SUCCESS"
    """Transaction succeeded.."""
    FAILED = "FAILED"
    """Transaction failed."""
    PENDING = "PENDING"
    """Transaction has been initiated and is currently in-flight."""
    NOT_STARTED = "NOT_STARTED"
    """For transaction type PAYMENT_REQUEST only. No payments have been made to a payment request."""
    EXPIRED = "EXPIRED"
    """For transaction type PAYMENT_REQUEST only. A payment request has expired."""
    CANCELLED = "CANCELLED"
    """For transaction type PAYMENT_REQUEST only."""
