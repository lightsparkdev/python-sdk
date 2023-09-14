# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.RiskRating import RiskRating
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .RiskRating import RiskRating


@dataclass
class ScreenNodeOutput:
    requester: Requester

    rating: RiskRating


FRAGMENT = """
fragment ScreenNodeOutputFragment on ScreenNodeOutput {
    __typename
    screen_node_output_rating: rating
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ScreenNodeOutput:
    return ScreenNodeOutput(
        requester=requester,
        rating=parse_enum(RiskRating, obj["screen_node_output_rating"]),
    )
