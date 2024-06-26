# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.utils.enums import parse_enum, parse_enum_optional

from .OnChainFeeTarget import OnChainFeeTarget
from .WithdrawalMode import WithdrawalMode


@dataclass
class RequestWithdrawalInput:

    node_id: str
    """The node from which you'd like to make the withdrawal."""

    bitcoin_address: str
    """The bitcoin address where the withdrawal should be sent."""

    amount_sats: int
    """The amount you want to withdraw from this node in Satoshis. Use the special value -1 to withdrawal all funds from this node."""

    withdrawal_mode: WithdrawalMode
    """The strategy that should be used to withdraw the funds from this node."""

    idempotency_key: Optional[str]
    """The idempotency key of the request. The same result will be returned for the same idempotency key."""

    fee_target: Optional[OnChainFeeTarget]
    """The target of the fee that should be used when crafting the L1 transaction. You should only set `fee_target` or `sats_per_vbyte`. If neither of them is set, default value of MEDIUM will be used as `fee_target`."""

    sats_per_vbyte: Optional[int]
    """A manual fee rate set in sat/vbyte that should be used when crafting the L1 transaction. You should only set `fee_target` or `sats_per_vbyte`"""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "request_withdrawal_input_node_id": self.node_id,
            "request_withdrawal_input_bitcoin_address": self.bitcoin_address,
            "request_withdrawal_input_amount_sats": self.amount_sats,
            "request_withdrawal_input_withdrawal_mode": self.withdrawal_mode.value,
            "request_withdrawal_input_idempotency_key": self.idempotency_key,
            "request_withdrawal_input_fee_target": (
                self.fee_target.value if self.fee_target else None
            ),
            "request_withdrawal_input_sats_per_vbyte": self.sats_per_vbyte,
        }


def from_json(obj: Mapping[str, Any]) -> RequestWithdrawalInput:
    return RequestWithdrawalInput(
        node_id=obj["request_withdrawal_input_node_id"],
        bitcoin_address=obj["request_withdrawal_input_bitcoin_address"],
        amount_sats=obj["request_withdrawal_input_amount_sats"],
        withdrawal_mode=parse_enum(
            WithdrawalMode, obj["request_withdrawal_input_withdrawal_mode"]
        ),
        idempotency_key=obj["request_withdrawal_input_idempotency_key"],
        fee_target=parse_enum_optional(
            OnChainFeeTarget, obj["request_withdrawal_input_fee_target"]
        ),
        sats_per_vbyte=obj["request_withdrawal_input_sats_per_vbyte"],
    )
