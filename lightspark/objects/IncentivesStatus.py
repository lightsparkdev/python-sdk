# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class IncentivesStatus(Enum):
    """Describes the status of the incentives for this invitation."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    PENDING = "PENDING"
    """The invitation is eligible for incentives in its current state. When it is claimed, we will reassess."""
    VALIDATED = "VALIDATED"
    """The incentives have been validated."""
    INELIGIBLE = "INELIGIBLE"
    """This invitation is not eligible for incentives. A more detailed reason can be found in the `incentives_ineligibility_reason` field."""
