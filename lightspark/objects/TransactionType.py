# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class TransactionType(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    OUTGOING_PAYMENT = "OUTGOING_PAYMENT"
    """Transactions initiated from a Lightspark node on Lightning Network."""
    INCOMING_PAYMENT = "INCOMING_PAYMENT"
    """Transactions received by a Lightspark node on Lightning Network."""
    ROUTED = "ROUTED"
    """Transactions that forwarded payments through Lightspark nodes on Lightning Network."""
    L1_WITHDRAW = "L1_WITHDRAW"
    """Transactions on the Bitcoin blockchain to withdraw funds from a Lightspark node to a Bitcoin wallet."""
    L1_DEPOSIT = "L1_DEPOSIT"
    """Transactions on Bitcoin blockchain to fund a Lightspark node's wallet."""
    CHANNEL_OPEN = "CHANNEL_OPEN"
    """Transactions on Bitcoin blockchain to open a channel on Lightning Network funded by the local Lightspark node."""
    CHANNEL_CLOSE = "CHANNEL_CLOSE"
    """Transactions on Bitcoin blockchain to close a channel on Lightning Network where the balances are allocated back to local and remote nodes."""
    PAYMENT = "PAYMENT"
    """Transactions initiated from a Lightspark node on Lightning Network."""
    PAYMENT_REQUEST = "PAYMENT_REQUEST"
    """Payment requests from a Lightspark node on Lightning Network"""
    ROUTE = "ROUTE"
    """Transactions that forwarded payments through Lightspark nodes on Lightning Network."""
