# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class OutgoingPaymentAttemptStatus(Enum):
    """This is an enum of all potential statuses of a payment attempt made from a Lightspark Node."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    IN_FLIGHT = "IN_FLIGHT"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
