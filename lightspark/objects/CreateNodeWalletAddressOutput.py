# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .MultiSigAddressValidationParameters import MultiSigAddressValidationParameters
from .MultiSigAddressValidationParameters import (
    from_json as MultiSigAddressValidationParameters_from_json,
)


@dataclass
class CreateNodeWalletAddressOutput:

    requester: Requester

    node_id: str

    wallet_address: str

    multisig_wallet_address_validation_parameters: Optional[
        MultiSigAddressValidationParameters
    ]
    """Vaildation parameters for the 2-of-2 multisig address. None if the address is not a 2-of-2 multisig address."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_node_wallet_address_output_node": {"id": self.node_id},
            "create_node_wallet_address_output_wallet_address": self.wallet_address,
            "create_node_wallet_address_output_multisig_wallet_address_validation_parameters": (
                self.multisig_wallet_address_validation_parameters.to_json()
                if self.multisig_wallet_address_validation_parameters
                else None
            ),
        }


FRAGMENT = """
fragment CreateNodeWalletAddressOutputFragment on CreateNodeWalletAddressOutput {
    __typename
    create_node_wallet_address_output_node: node {
        id
    }
    create_node_wallet_address_output_wallet_address: wallet_address
    create_node_wallet_address_output_multisig_wallet_address_validation_parameters: multisig_wallet_address_validation_parameters {
        __typename
        multi_sig_address_validation_parameters_counterparty_funding_pubkey: counterparty_funding_pubkey
        multi_sig_address_validation_parameters_funding_pubkey_derivation_path: funding_pubkey_derivation_path
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> CreateNodeWalletAddressOutput:
    return CreateNodeWalletAddressOutput(
        requester=requester,
        node_id=obj["create_node_wallet_address_output_node"]["id"],
        wallet_address=obj["create_node_wallet_address_output_wallet_address"],
        multisig_wallet_address_validation_parameters=(
            MultiSigAddressValidationParameters_from_json(
                requester,
                obj[
                    "create_node_wallet_address_output_multisig_wallet_address_validation_parameters"
                ],
            )
            if obj[
                "create_node_wallet_address_output_multisig_wallet_address_validation_parameters"
            ]
            else None
        ),
    )
