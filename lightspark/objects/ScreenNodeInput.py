# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.ComplianceProvider import ComplianceProvider
from lightspark.utils.enums import parse_enum

from .ComplianceProvider import ComplianceProvider


@dataclass
class ScreenNodeInput:
    provider: ComplianceProvider
    """The compliance provider that is going to screen the node. You need to be a customer of the selected provider and store the API key on the Lightspark account setting page."""

    node_pubkey: str
    """The public key of the lightning node that needs to be screened."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "screen_node_input_provider": self.provider.value,
            "screen_node_input_node_pubkey": self.node_pubkey,
        }


def from_json(obj: Mapping[str, Any]) -> ScreenNodeInput:
    return ScreenNodeInput(
        provider=parse_enum(ComplianceProvider, obj["screen_node_input_provider"]),
        node_pubkey=obj["screen_node_input_node_pubkey"],
    )
