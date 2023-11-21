# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class ClaimUmaInvitationOutput:
    requester: Requester

    invitation_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "claim_uma_invitation_output_invitation": {"id": self.invitation_id},
        }


FRAGMENT = """
fragment ClaimUmaInvitationOutputFragment on ClaimUmaInvitationOutput {
    __typename
    claim_uma_invitation_output_invitation: invitation {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ClaimUmaInvitationOutput:
    return ClaimUmaInvitationOutput(
        requester=requester,
        invitation_id=obj["claim_uma_invitation_output_invitation"]["id"],
    )
