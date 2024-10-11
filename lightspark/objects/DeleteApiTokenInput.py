# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class DeleteApiTokenInput:

    api_token_id: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "delete_api_token_input_api_token_id": self.api_token_id,
        }


def from_json(obj: Mapping[str, Any]) -> DeleteApiTokenInput:
    return DeleteApiTokenInput(
        api_token_id=obj["delete_api_token_input_api_token_id"],
    )
