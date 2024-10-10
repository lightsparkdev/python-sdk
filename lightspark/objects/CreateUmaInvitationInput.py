# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class CreateUmaInvitationInput:
    inviter_uma: str
    """The UMA of the user creating the invitation. It will be used to identify the inviter when receiving the invitation."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_uma_invitation_input_inviter_uma": self.inviter_uma,
        }


def from_json(obj: Mapping[str, Any]) -> CreateUmaInvitationInput:
    return CreateUmaInvitationInput(
        inviter_uma=obj["create_uma_invitation_input_inviter_uma"],
    )
