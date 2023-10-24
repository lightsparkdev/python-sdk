# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.objects.SignablePayloadStatus import SignablePayloadStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .Entity import Entity
from .SignablePayloadStatus import SignablePayloadStatus


@dataclass
class SignablePayload(Entity):
    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    payload: str
    """The payload that needs to be signed."""

    derivation_path: str
    """The consistent method for generating the same set of accounts and wallets for a given private key"""

    status: SignablePayloadStatus
    """The status of the payload."""

    add_tweak: Optional[str]
    """The tweak value to add."""

    mul_tweak: Optional[str]
    """The tweak value to multiply."""

    signable_id: str
    """The signable this payload belongs to."""
    typename: str


FRAGMENT = """
fragment SignablePayloadFragment on SignablePayload {
    __typename
    signable_payload_id: id
    signable_payload_created_at: created_at
    signable_payload_updated_at: updated_at
    signable_payload_payload: payload
    signable_payload_derivation_path: derivation_path
    signable_payload_status: status
    signable_payload_add_tweak: add_tweak
    signable_payload_mul_tweak: mul_tweak
    signable_payload_signable: signable {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> SignablePayload:
    return SignablePayload(
        requester=requester,
        typename="SignablePayload",
        id=obj["signable_payload_id"],
        created_at=datetime.fromisoformat(obj["signable_payload_created_at"]),
        updated_at=datetime.fromisoformat(obj["signable_payload_updated_at"]),
        payload=obj["signable_payload_payload"],
        derivation_path=obj["signable_payload_derivation_path"],
        status=parse_enum(SignablePayloadStatus, obj["signable_payload_status"]),
        add_tweak=obj["signable_payload_add_tweak"],
        mul_tweak=obj["signable_payload_mul_tweak"],
        signable_id=obj["signable_payload_signable"]["id"],
    )
