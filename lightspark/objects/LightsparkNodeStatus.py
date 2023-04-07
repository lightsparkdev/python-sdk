# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class LightsparkNodeStatus(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    CREATED = "CREATED"
    DEPLOYED = "DEPLOYED"
    STARTED = "STARTED"
    SYNCING = "SYNCING"
    READY = "READY"
    STOPPED = "STOPPED"
    TERMINATED = "TERMINATED"
    WALLET_LOCKED = "WALLET_LOCKED"
    FAILED_TO_DEPLOY = "FAILED_TO_DEPLOY"
