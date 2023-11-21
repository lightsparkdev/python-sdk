# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.RegionCode import RegionCode
from lightspark.utils.enums import parse_enum

from .RegionCode import RegionCode


@dataclass
class ClaimUmaInvitationWithIncentivesInput:
    invitation_code: str

    invitee_uma: str

    invitee_phone_hash: str

    invitee_region: RegionCode

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
