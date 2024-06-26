# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class ClaimUmaInvitationInput:
    invitation_code: str
    """The unique code that identifies this invitation and was shared by the inviter."""

    invitee_uma: str
    """The UMA of the user claiming the invitation. It will be sent to the inviter so that they can start transacting with the invitee."""

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
