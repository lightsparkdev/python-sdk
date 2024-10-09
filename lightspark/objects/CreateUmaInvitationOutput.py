# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateUmaInvitationOutput:

    requester: Requester

    invitation_id: str
    """The created invitation in the form of a string identifier."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_uma_invitation_output_invitation": {"id": self.invitation_id},
        }


FRAGMENT = """
fragment CreateUmaInvitationOutputFragment on CreateUmaInvitationOutput {
    __typename
    create_uma_invitation_output_invitation: invitation {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateUmaInvitationOutput:
    return CreateUmaInvitationOutput(
        requester=requester,
        invitation_id=obj["create_uma_invitation_output_invitation"]["id"],
    )
