# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class FundNodeInput:

    node_id: str

    amount_sats: Optional[int]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "fund_node_input_node_id": self.node_id,
            "fund_node_input_amount_sats": self.amount_sats,
        }


def from_json(obj: Mapping[str, Any]) -> FundNodeInput:
    return FundNodeInput(
        node_id=obj["fund_node_input_node_id"],
        amount_sats=obj["fund_node_input_amount_sats"],
    )
