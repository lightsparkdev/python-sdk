# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.utils.enums import parse_enum

from .RegionCode import RegionCode


@dataclass
class ClaimUmaInvitationWithIncentivesInput:

    invitation_code: str
    """The unique code that identifies this invitation and was shared by the inviter."""

    invitee_uma: str
    """The UMA of the user claiming the invitation. It will be sent to the inviter so that they can start transacting with the invitee."""

    invitee_phone_hash: str
    """The phone hash of the user getting the invitation."""

    invitee_region: RegionCode
    """The region of the user getting the invitation."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "claim_uma_invitation_with_incentives_input_invitation_code": self.invitation_code,
            "claim_uma_invitation_with_incentives_input_invitee_uma": self.invitee_uma,
            "claim_uma_invitation_with_incentives_input_invitee_phone_hash": self.invitee_phone_hash,
            "claim_uma_invitation_with_incentives_input_invitee_region": self.invitee_region.value,
        }


def from_json(obj: Mapping[str, Any]) -> ClaimUmaInvitationWithIncentivesInput:
    return ClaimUmaInvitationWithIncentivesInput(
        invitation_code=obj[
            "claim_uma_invitation_with_incentives_input_invitation_code"
        ],
        invitee_uma=obj["claim_uma_invitation_with_incentives_input_invitee_uma"],
        invitee_phone_hash=obj[
            "claim_uma_invitation_with_incentives_input_invitee_phone_hash"
        ],
        invitee_region=parse_enum(
            RegionCode, obj["claim_uma_invitation_with_incentives_input_invitee_region"]
        ),
    )
