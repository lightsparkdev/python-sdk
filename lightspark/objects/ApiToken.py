# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_list

from .Entity import Entity
from .Permission import Permission


@dataclass
class ApiToken(Entity):
    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    client_id: str
    """An opaque identifier that should be used as a client_id (or username) in the HTTP Basic Authentication scheme when issuing requests against the Lightspark API."""

    name: str
    """An arbitrary name chosen by the creator of the token to help identify the token in the list of tokens that have been created for the account."""

    permissions: List[Permission]
    """A list of permissions granted to the token."""
    typename: str


FRAGMENT = """
fragment ApiTokenFragment on ApiToken {
    __typename
    api_token_id: id
    api_token_created_at: created_at
    api_token_updated_at: updated_at
    api_token_client_id: client_id
    api_token_name: name
    api_token_permissions: permissions
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ApiToken:
    return ApiToken(
        requester=requester,
        typename="ApiToken",
        id=obj["api_token_id"],
        created_at=obj["api_token_created_at"],
        updated_at=obj["api_token_updated_at"],
        client_id=obj["api_token_client_id"],
        name=obj["api_token_name"],
        permissions=parse_enum_list(Permission, obj["api_token_permissions"]),
    )
