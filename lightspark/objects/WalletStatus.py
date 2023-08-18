# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class WalletStatus(Enum):
    """This is an enum of the potential statuses that your Lightspark wallet can take."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    NOT_SETUP = "NOT_SETUP"
    """The wallet has not been set up yet and is ready to be deployed. This is the default status after the first login."""
    DEPLOYING = "DEPLOYING"
    """The wallet is currently being deployed in the Lightspark infrastructure."""
    DEPLOYED = "DEPLOYED"
    """The wallet has been deployed in the Lightspark infrastructure and is ready to be initialized."""
    INITIALIZING = "INITIALIZING"
    """The wallet is currently being initialized."""
    READY = "READY"
    """The wallet is available and ready to be used."""
    UNAVAILABLE = "UNAVAILABLE"
    """The wallet is temporarily available, due to a transient issue or a scheduled maintenance."""
    FAILED = "FAILED"
    """The wallet had an unrecoverable failure. This status is not expected to happend and will be investigated by the Lightspark team."""
    TERMINATING = "TERMINATING"
    """The wallet is being terminated."""
    TERMINATED = "TERMINATED"
    """The wallet has been terminated and is not available in the Lightspark infrastructure anymore. It is not connected to the Lightning network and its funds can only be accessed using the Funds Recovery flow."""
