# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.objects.CryptoSanctionsScreeningProvider import (
    CryptoSanctionsScreeningProvider,
)
from lightspark.utils.enums import parse_enum

from .CryptoSanctionsScreeningProvider import CryptoSanctionsScreeningProvider


@dataclass
class ScreenBitcoinAddressesInput:
    provider: CryptoSanctionsScreeningProvider

    addresses: List[str]


def from_json(obj: Mapping[str, Any]) -> ScreenBitcoinAddressesInput:
    return ScreenBitcoinAddressesInput(
        provider=parse_enum(
            CryptoSanctionsScreeningProvider,
            obj["screen_bitcoin_addresses_input_provider"],
        ),
        addresses=obj["screen_bitcoin_addresses_input_addresses"],
    )
