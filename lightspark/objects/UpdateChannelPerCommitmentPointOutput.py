# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class UpdateChannelPerCommitmentPointOutput:
    requester: Requester

    channel_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "update_channel_per_commitment_point_output_channel": {
                "id": self.channel_id
            },
        }


FRAGMENT = """
fragment UpdateChannelPerCommitmentPointOutputFragment on UpdateChannelPerCommitmentPointOutput {
    __typename
    update_channel_per_commitment_point_output_channel: channel {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> UpdateChannelPerCommitmentPointOutput:
    return UpdateChannelPerCommitmentPointOutput(
        requester=requester,
        channel_id=obj["update_channel_per_commitment_point_output_channel"]["id"],
    )
