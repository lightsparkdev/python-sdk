# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .ApiToken import ApiToken
from .ApiToken import from_json as ApiToken_from_json


@dataclass
class CreateApiTokenOutput:
    requester: Requester

    api_token: ApiToken
    """The API Token that has been created."""

    client_secret: str
    """The secret that should be used to authenticate against our API.
This secret is not stored and will never be available again after this. You must keep this secret secure as it grants access to your account."""


FRAGMENT = """
fragment CreateApiTokenOutputFragment on CreateApiTokenOutput {
    __typename
    create_api_token_output_api_token: api_token {
        __typename
        api_token_id: id
        api_token_created_at: created_at
        api_token_updated_at: updated_at
        api_token_client_id: client_id
        api_token_name: name
        api_token_permissions: permissions
    }
    create_api_token_output_client_secret: client_secret
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> CreateApiTokenOutput:
    return CreateApiTokenOutput(
        requester=requester,
        api_token=ApiToken_from_json(
            requester, obj["create_api_token_output_api_token"]
        ),
        client_secret=obj["create_api_token_output_client_secret"],
    )
