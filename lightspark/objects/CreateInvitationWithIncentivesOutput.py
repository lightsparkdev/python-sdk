# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateInvitationWithIncentivesOutput:
    requester: Requester

    invitation_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_invitation_with_incentives_output_invitation": {
                "id": self.invitation_id
            },
        }


FRAGMENT = """
fragment CreateInvitationWithIncentivesOutputFragment on CreateInvitationWithIncentivesOutput {
    __typename
    create_invitation_with_incentives_output_invitation: invitation {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateInvitationWithIncentivesOutput:
    return CreateInvitationWithIncentivesOutput(
        requester=requester,
        invitation_id=obj["create_invitation_with_incentives_output_invitation"]["id"],
    )
