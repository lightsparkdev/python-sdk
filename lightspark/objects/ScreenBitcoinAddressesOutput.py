# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_list

from .RiskRating import RiskRating


@dataclass
class ScreenBitcoinAddressesOutput:
    requester: Requester

    ratings: List[RiskRating]


FRAGMENT = """
fragment ScreenBitcoinAddressesOutputFragment on ScreenBitcoinAddressesOutput {
    __typename
    screen_bitcoin_addresses_output_ratings: ratings
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ScreenBitcoinAddressesOutput:
    return ScreenBitcoinAddressesOutput(
        requester=requester,
        ratings=parse_enum_list(
            RiskRating, obj["screen_bitcoin_addresses_output_ratings"]
        ),
    )
