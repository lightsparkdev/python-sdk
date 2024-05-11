# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class RemoteSigningSubEventType(Enum):
    """This is an enum of the potential sub-event types for Remote Signing webook events."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    ECDH = "ECDH"
    GET_PER_COMMITMENT_POINT = "GET_PER_COMMITMENT_POINT"
    RELEASE_PER_COMMITMENT_SECRET = "RELEASE_PER_COMMITMENT_SECRET"
    SIGN_INVOICE = "SIGN_INVOICE"
    DERIVE_KEY_AND_SIGN = "DERIVE_KEY_AND_SIGN"
    RELEASE_PAYMENT_PREIMAGE = "RELEASE_PAYMENT_PREIMAGE"
    REQUEST_INVOICE_PAYMENT_HASH = "REQUEST_INVOICE_PAYMENT_HASH"
    REVEAL_COUNTERPARTY_PER_COMMITMENT_SECRET = (
        "REVEAL_COUNTERPARTY_PER_COMMITMENT_SECRET"
    )
    VLS_MESSAGE = "VLS_MESSAGE"
