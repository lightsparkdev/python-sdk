# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .Entity import Entity
from .IncentivesIneligibilityReason import IncentivesIneligibilityReason
from .IncentivesStatus import IncentivesStatus


@dataclass
class UmaInvitation(Entity):
    """This is an object representing an UMA.ME invitation."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    code: str
    """The code that uniquely identifies this invitation."""

    url: str
    """The URL where this invitation can be claimed."""

    inviter_uma: str
    """The UMA of the user who created the invitation."""

    invitee_uma: Optional[str]
    """The UMA of the user who claimed the invitation."""

    incentives_status: IncentivesStatus
    """The current status of the incentives that may be tied to this invitation."""

    incentives_ineligibility_reason: Optional[IncentivesIneligibilityReason]
    """The reason why the invitation is not eligible for incentives, if applicable."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "UmaInvitation",
            "uma_invitation_id": self.id,
            "uma_invitation_created_at": self.created_at.isoformat(),
            "uma_invitation_updated_at": self.updated_at.isoformat(),
            "uma_invitation_code": self.code,
            "uma_invitation_url": self.url,
            "uma_invitation_inviter_uma": self.inviter_uma,
            "uma_invitation_invitee_uma": self.invitee_uma,
            "uma_invitation_incentives_status": self.incentives_status.value,
            "uma_invitation_incentives_ineligibility_reason": self.incentives_ineligibility_reason.value
            if self.incentives_ineligibility_reason
            else None,
        }


FRAGMENT = """
fragment UmaInvitationFragment on UmaInvitation {
    __typename
    uma_invitation_id: id
    uma_invitation_created_at: created_at
    uma_invitation_updated_at: updated_at
    uma_invitation_code: code
    uma_invitation_url: url
    uma_invitation_inviter_uma: inviter_uma
    uma_invitation_invitee_uma: invitee_uma
    uma_invitation_incentives_status: incentives_status
    uma_invitation_incentives_ineligibility_reason: incentives_ineligibility_reason
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> UmaInvitation:
    return UmaInvitation(
        requester=requester,
        typename="UmaInvitation",
        id=obj["uma_invitation_id"],
        created_at=datetime.fromisoformat(obj["uma_invitation_created_at"]),
        updated_at=datetime.fromisoformat(obj["uma_invitation_updated_at"]),
        code=obj["uma_invitation_code"],
        url=obj["uma_invitation_url"],
        inviter_uma=obj["uma_invitation_inviter_uma"],
        invitee_uma=obj["uma_invitation_invitee_uma"],
        incentives_status=parse_enum(
            IncentivesStatus, obj["uma_invitation_incentives_status"]
        ),
        incentives_ineligibility_reason=parse_enum_optional(
            IncentivesIneligibilityReason,
            obj["uma_invitation_incentives_ineligibility_reason"],
        ),
    )
