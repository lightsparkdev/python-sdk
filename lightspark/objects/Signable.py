# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .Entity import Entity


@dataclass
class Signable(Entity):
    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""
    typename: str


FRAGMENT = """
fragment SignableFragment on Signable {
    __typename
    signable_id: id
    signable_created_at: created_at
    signable_updated_at: updated_at
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Signable:
    return Signable(
        requester=requester,
        typename="Signable",
        id=obj["signable_id"],
        created_at=datetime.fromisoformat(obj["signable_created_at"]),
        updated_at=datetime.fromisoformat(obj["signable_updated_at"]),
    )
