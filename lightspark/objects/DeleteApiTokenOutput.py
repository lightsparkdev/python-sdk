# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class DeleteApiTokenOutput:
    requester: Requester

    account_id: str


FRAGMENT = """
fragment DeleteApiTokenOutputFragment on DeleteApiTokenOutput {
    __typename
    delete_api_token_output_account: account {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> DeleteApiTokenOutput:
    return DeleteApiTokenOutput(
        requester=requester,
        account_id=obj["delete_api_token_output_account"]["id"],
    )
