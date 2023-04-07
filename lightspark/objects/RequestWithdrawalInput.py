# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.WithdrawalMode import WithdrawalMode
from lightspark.utils.enums import parse_enum

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


def from_json(obj: Mapping[str, Any]) -> RequestWithdrawalInput:
    return RequestWithdrawalInput(
        node_id=obj["request_withdrawal_input_node_id"],
        bitcoin_address=obj["request_withdrawal_input_bitcoin_address"],
        amount_sats=obj["request_withdrawal_input_amount_sats"],
        withdrawal_mode=parse_enum(
            WithdrawalMode, obj["request_withdrawal_input_withdrawal_mode"]
        ),
    )
