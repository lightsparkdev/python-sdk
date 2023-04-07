# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class RequestWithdrawalOutput:
    requester: Requester

    request_id: str
    """The request that is created for this withdrawal."""


FRAGMENT = """
fragment RequestWithdrawalOutputFragment on RequestWithdrawalOutput {
    __typename
    request_withdrawal_output_request: request {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> RequestWithdrawalOutput:
    return RequestWithdrawalOutput(
        requester=requester,
        request_id=obj["request_withdrawal_output_request"]["id"],
    )
