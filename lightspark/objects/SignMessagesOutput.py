# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .SignablePayload import SignablePayload
from .SignablePayload import from_json as SignablePayload_from_json


@dataclass
class SignMessagesOutput:
    requester: Requester

    signed_payloads: List[SignablePayload]


FRAGMENT = """
fragment SignMessagesOutputFragment on SignMessagesOutput {
    __typename
    sign_messages_output_signed_payloads: signed_payloads {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> SignMessagesOutput:
    return SignMessagesOutput(
        requester=requester,
        signed_payloads=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: SignablePayload_from_json(requester, e),
                obj["sign_messages_output_signed_payloads"],
            )
        ),
    )
