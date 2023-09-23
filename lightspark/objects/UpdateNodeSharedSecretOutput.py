# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class UpdateNodeSharedSecretOutput:
    requester: Requester

    node_id: str


FRAGMENT = """
fragment UpdateNodeSharedSecretOutputFragment on UpdateNodeSharedSecretOutput {
    __typename
    update_node_shared_secret_output_node: node {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> UpdateNodeSharedSecretOutput:
    return UpdateNodeSharedSecretOutput(
        requester=requester,
        node_id=obj["update_node_shared_secret_output_node"]["id"],
    )
