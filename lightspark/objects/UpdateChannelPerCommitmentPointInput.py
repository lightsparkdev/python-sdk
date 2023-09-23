# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class UpdateChannelPerCommitmentPointInput:
    channel_id: str

    per_commitment_point: str

    per_commitment_point_index: int


def from_json(obj: Mapping[str, Any]) -> UpdateChannelPerCommitmentPointInput:
    return UpdateChannelPerCommitmentPointInput(
        channel_id=obj["update_channel_per_commitment_point_input_channel_id"],
        per_commitment_point=obj[
            "update_channel_per_commitment_point_input_per_commitment_point"
        ],
        per_commitment_point_index=obj[
            "update_channel_per_commitment_point_input_per_commitment_point_index"
        ],
    )
