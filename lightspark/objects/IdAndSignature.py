# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class IdAndSignature:

    id: str
    """The id of the message."""

    signature: str
    """The signature of the message."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "id_and_signature_id": self.id,
            "id_and_signature_signature": self.signature,
        }


def from_json(obj: Mapping[str, Any]) -> IdAndSignature:
    return IdAndSignature(
        id=obj["id_and_signature_id"],
        signature=obj["id_and_signature_signature"],
    )
