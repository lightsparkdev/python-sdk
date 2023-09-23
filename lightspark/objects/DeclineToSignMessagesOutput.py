# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .SignablePayload import SignablePayload
from .SignablePayload import from_json as SignablePayload_from_json


@dataclass
class DeclineToSignMessagesOutput:
    requester: Requester

    declined_payloads: List[SignablePayload]


FRAGMENT = """
fragment DeclineToSignMessagesOutputFragment on DeclineToSignMessagesOutput {
    __typename
    decline_to_sign_messages_output_declined_payloads: declined_payloads {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> DeclineToSignMessagesOutput:
    return DeclineToSignMessagesOutput(
        requester=requester,
        declined_payloads=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: SignablePayload_from_json(requester, e),
                obj["decline_to_sign_messages_output_declined_payloads"],
            )
        ),
    )
