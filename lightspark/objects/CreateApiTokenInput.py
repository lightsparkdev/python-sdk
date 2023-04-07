# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.utils.enums import parse_enum_list

from .Permission import Permission


@dataclass
class CreateApiTokenInput:
    name: str
    """An arbitrary name that the user can choose to identify the API token in a list."""

    permissions: List[Permission]
    """List of permissions to grant to the API token"""


def from_json(obj: Mapping[str, Any]) -> CreateApiTokenInput:
    return CreateApiTokenInput(
        name=obj["create_api_token_input_name"],
        permissions=parse_enum_list(
            Permission, obj["create_api_token_input_permissions"]
        ),
    )
