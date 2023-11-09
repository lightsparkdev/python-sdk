# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateNodeWalletAddressOutput:
    requester: Requester

    node_id: str

    wallet_address: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_node_wallet_address_output_node": {"id": self.node_id},
            "create_node_wallet_address_output_wallet_address": self.wallet_address,
        }


FRAGMENT = """
fragment CreateNodeWalletAddressOutputFragment on CreateNodeWalletAddressOutput {
    __typename
    create_node_wallet_address_output_node: node {
        id
    }
    create_node_wallet_address_output_wallet_address: wallet_address
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateNodeWalletAddressOutput:
    return CreateNodeWalletAddressOutput(
        requester=requester,
        node_id=obj["create_node_wallet_address_output_node"]["id"],
        wallet_address=obj["create_node_wallet_address_output_wallet_address"],
    )
