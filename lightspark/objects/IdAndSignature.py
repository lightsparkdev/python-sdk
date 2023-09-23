# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class IdAndSignature:
    id: str

    signature: str


def from_json(obj: Mapping[str, Any]) -> IdAndSignature:
    return IdAndSignature(
        id=obj["id_and_signature_id"],
        signature=obj["id_and_signature_signature"],
    )
