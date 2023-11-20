# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class ClaimUmaInvitationInput:
    invitation_code: str

    invitee_uma: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "claim_uma_invitation_input_invitation_code": self.invitation_code,
            "claim_uma_invitation_input_invitee_uma": self.invitee_uma,
        }


def from_json(obj: Mapping[str, Any]) -> ClaimUmaInvitationInput:
    return ClaimUmaInvitationInput(
        invitation_code=obj["claim_uma_invitation_input_invitation_code"],
        invitee_uma=obj["claim_uma_invitation_input_invitee_uma"],
    )
