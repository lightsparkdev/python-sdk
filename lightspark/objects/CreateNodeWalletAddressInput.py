# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class CreateNodeWalletAddressInput:
    node_id: str


def from_json(obj: Mapping[str, Any]) -> CreateNodeWalletAddressInput:
    return CreateNodeWalletAddressInput(
        node_id=obj["create_node_wallet_address_input_node_id"],
    )
