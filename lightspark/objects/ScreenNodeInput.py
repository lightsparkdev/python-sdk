# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.ComplianceProvider import ComplianceProvider
from lightspark.utils.enums import parse_enum

from .ComplianceProvider import ComplianceProvider


@dataclass
class ScreenNodeInput:
    provider: ComplianceProvider

    node_pubkey: str


def from_json(obj: Mapping[str, Any]) -> ScreenNodeInput:
    return ScreenNodeInput(
        provider=parse_enum(ComplianceProvider, obj["screen_node_input_provider"]),
        node_pubkey=obj["screen_node_input_node_pubkey"],
    )
