# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class ReleaseChannelPerCommitmentSecretInput:
    channel_id: str
    """The unique identifier of the channel."""

    per_commitment_secret: str
    """The per-commitment secret to be released."""

    per_commitment_index: int
    """The index associated with the per-commitment secret."""


def from_json(obj: Mapping[str, Any]) -> ReleaseChannelPerCommitmentSecretInput:
    return ReleaseChannelPerCommitmentSecretInput(
        channel_id=obj["release_channel_per_commitment_secret_input_channel_id"],
        per_commitment_secret=obj[
            "release_channel_per_commitment_secret_input_per_commitment_secret"
        ],
        per_commitment_index=obj[
            "release_channel_per_commitment_secret_input_per_commitment_index"
        ],
    )
