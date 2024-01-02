# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.WithdrawalMode import WithdrawalMode
from lightspark.utils.enums import parse_enum

from .WithdrawalMode import WithdrawalMode


@dataclass
class WithdrawalFeeEstimateInput:
    node_id: str
    """The node from which you'd like to make the withdrawal."""

    amount_sats: int
    """The amount you want to withdraw from this node in Satoshis. Use the special value -1 to withdrawal all funds from this node."""

    withdrawal_mode: WithdrawalMode
    """The strategy that should be used to withdraw the funds from this node."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "withdrawal_fee_estimate_input_node_id": self.node_id,
            "withdrawal_fee_estimate_input_amount_sats": self.amount_sats,
            "withdrawal_fee_estimate_input_withdrawal_mode": self.withdrawal_mode.value,
        }


def from_json(obj: Mapping[str, Any]) -> WithdrawalFeeEstimateInput:
    return WithdrawalFeeEstimateInput(
        node_id=obj["withdrawal_fee_estimate_input_node_id"],
        amount_sats=obj["withdrawal_fee_estimate_input_amount_sats"],
        withdrawal_mode=parse_enum(
            WithdrawalMode, obj["withdrawal_fee_estimate_input_withdrawal_mode"]
        ),
    )
