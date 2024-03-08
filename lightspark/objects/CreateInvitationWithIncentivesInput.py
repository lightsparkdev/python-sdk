# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.RegionCode import RegionCode
from lightspark.utils.enums import parse_enum

from .RegionCode import RegionCode


@dataclass
class CreateInvitationWithIncentivesInput:
    inviter_uma: str
    """The UMA of the user creating the invitation. It will be used to identify the inviter when receiving the invitation."""

    inviter_phone_hash: str
    """The phone hash of the user creating the invitation."""

    inviter_region: RegionCode
    """The region of the user creating the invitation."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_invitation_with_incentives_input_inviter_uma": self.inviter_uma,
            "create_invitation_with_incentives_input_inviter_phone_hash": self.inviter_phone_hash,
            "create_invitation_with_incentives_input_inviter_region": self.inviter_region.value,
        }


def from_json(obj: Mapping[str, Any]) -> CreateInvitationWithIncentivesInput:
    return CreateInvitationWithIncentivesInput(
        inviter_uma=obj["create_invitation_with_incentives_input_inviter_uma"],
        inviter_phone_hash=obj[
            "create_invitation_with_incentives_input_inviter_phone_hash"
        ],
        inviter_region=parse_enum(
            RegionCode, obj["create_invitation_with_incentives_input_inviter_region"]
        ),
    )
