# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class ReleaseChannelPerCommitmentSecretOutput:
    requester: Requester

    channel_id: str


FRAGMENT = """
fragment ReleaseChannelPerCommitmentSecretOutputFragment on ReleaseChannelPerCommitmentSecretOutput {
    __typename
    release_channel_per_commitment_secret_output_channel: channel {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ReleaseChannelPerCommitmentSecretOutput:
    return ReleaseChannelPerCommitmentSecretOutput(
        requester=requester,
        channel_id=obj["release_channel_per_commitment_secret_output_channel"]["id"],
    )
