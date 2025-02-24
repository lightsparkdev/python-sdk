# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class ClaimUmaInvitationWithIncentivesOutput:

    requester: Requester

    invitation_id: str
    """An UMA.ME invitation object."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "claim_uma_invitation_with_incentives_output_invitation": {
                "id": self.invitation_id
            },
        }


FRAGMENT = """
fragment ClaimUmaInvitationWithIncentivesOutputFragment on ClaimUmaInvitationWithIncentivesOutput {
    __typename
    claim_uma_invitation_with_incentives_output_invitation: invitation {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ClaimUmaInvitationWithIncentivesOutput:
    return ClaimUmaInvitationWithIncentivesOutput(
        requester=requester,
        invitation_id=obj["claim_uma_invitation_with_incentives_output_invitation"][
            "id"
        ],
    )
