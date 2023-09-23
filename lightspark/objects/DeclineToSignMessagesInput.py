# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping


@dataclass
class DeclineToSignMessagesInput:
    payload_ids: List[str]
    """List of payload ids to decline to sign because validation failed."""


def from_json(obj: Mapping[str, Any]) -> DeclineToSignMessagesInput:
    return DeclineToSignMessagesInput(
        payload_ids=obj["decline_to_sign_messages_input_payload_ids"],
    )
