# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from .IdAndSignature import IdAndSignature
from .IdAndSignature import from_json as IdAndSignature_from_json


@dataclass
class SignMessagesInput:
    signatures: List[IdAndSignature]
    """The list of the message ids and signatures."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "sign_messages_input_signatures": [e.to_json() for e in self.signatures],
        }


def from_json(obj: Mapping[str, Any]) -> SignMessagesInput:
    return SignMessagesInput(
        signatures=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: IdAndSignature_from_json(e),
                obj["sign_messages_input_signatures"],
            )
        ),
    )
