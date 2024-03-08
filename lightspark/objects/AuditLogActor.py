# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from lightspark.exceptions import LightsparkException
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_list

from .Entity import Entity


@dataclass
class AuditLogActor(Entity):
    """Audit log actor who called the GraphQL mutation"""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": self.typename,
            "audit_log_actor_id": self.id,
            "audit_log_actor_created_at": self.created_at.isoformat(),
            "audit_log_actor_updated_at": self.updated_at.isoformat(),
        }


FRAGMENT = """
fragment AuditLogActorFragment on AuditLogActor {
    __typename
    ... on ApiToken {
        __typename
        api_token_id: id
        api_token_created_at: created_at
        api_token_updated_at: updated_at
        api_token_client_id: client_id
        api_token_name: name
        api_token_permissions: permissions
        api_token_is_deleted: is_deleted
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> AuditLogActor:
    if obj["__typename"] == "ApiToken":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.ApiToken import ApiToken

        return ApiToken(
            requester=requester,
            typename="ApiToken",
            id=obj["api_token_id"],
            created_at=datetime.fromisoformat(obj["api_token_created_at"]),
            updated_at=datetime.fromisoformat(obj["api_token_updated_at"]),
            client_id=obj["api_token_client_id"],
            name=obj["api_token_name"],
            permissions=parse_enum_list(Permission, obj["api_token_permissions"]),
            is_deleted=obj["api_token_is_deleted"],
        )
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface AuditLogActor corresponding to the typename={graphql_typename}",
    )
