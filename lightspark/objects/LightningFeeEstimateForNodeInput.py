# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class LightningFeeEstimateForNodeInput:
    node_id: str
    """The node from where you want to send the payment."""

    destination_node_public_key: str
    """The public key of the node that you want to pay."""

    amount_msats: int
    """The payment amount expressed in msats."""


def from_json(obj: Mapping[str, Any]) -> LightningFeeEstimateForNodeInput:
    return LightningFeeEstimateForNodeInput(
        node_id=obj["lightning_fee_estimate_for_node_input_node_id"],
        destination_node_public_key=obj[
            "lightning_fee_estimate_for_node_input_destination_node_public_key"
        ],
        amount_msats=obj["lightning_fee_estimate_for_node_input_amount_msats"],
    )
