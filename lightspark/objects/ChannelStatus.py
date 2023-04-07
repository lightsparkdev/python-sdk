# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class ChannelStatus(Enum):
    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    OK = "OK"
    """The channel is online and ready to send and receive funds."""
    PENDING = "PENDING"
    """The channel has been created, but the Bitcoin transaction that initiates it still needs to be confirmed on the Bitcoin blockchain."""
    OFFLINE = "OFFLINE"
    """The channel is not available, likely because the peer is not online."""
    UNBALANCED_FOR_SEND = "UNBALANCED_FOR_SEND"
    """The channel is behaving properly, but its remote balance is much higher than its local balance so it is not balanced properly for sending funds out."""
    UNBALANCED_FOR_RECEIVE = "UNBALANCED_FOR_RECEIVE"
    """The channel is behaving properly, but its remote balance is much lower than its local balance so it is not balanced properly for receiving funds."""
    CLOSED = "CLOSED"
    """The channel has been closed. Information about the channel is still available for historical purposes but the channel cannot be used anymore."""
    ERROR = "ERROR"
    """Something unexpected happened and we cannot determine the status of this channel. Please try again later or contact the support."""
