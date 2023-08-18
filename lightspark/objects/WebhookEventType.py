# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class WebhookEventType(Enum):
    """This is an enum of the potential event types that can be associated with your Lightspark wallets."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    PAYMENT_FINISHED = "PAYMENT_FINISHED"
    NODE_STATUS = "NODE_STATUS"
    WALLET_STATUS = "WALLET_STATUS"
    WALLET_OUTGOING_PAYMENT_FINISHED = "WALLET_OUTGOING_PAYMENT_FINISHED"
    WALLET_INCOMING_PAYMENT_FINISHED = "WALLET_INCOMING_PAYMENT_FINISHED"
    WALLET_WITHDRAWAL_FINISHED = "WALLET_WITHDRAWAL_FINISHED"
    WALLET_FUNDS_RECEIVED = "WALLET_FUNDS_RECEIVED"
    REMOTE_SIGNING = "REMOTE_SIGNING"
