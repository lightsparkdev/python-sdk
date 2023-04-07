# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class Secret:
    requester: Requester

    encrypted_value: str

    cipher: str


FRAGMENT = """
fragment SecretFragment on Secret {
    __typename
    secret_encrypted_value: encrypted_value
    secret_cipher: cipher
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Secret:
    return Secret(
        requester=requester,
        encrypted_value=obj["secret_encrypted_value"],
        cipher=obj["secret_cipher"],
    )
