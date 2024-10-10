# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class FundNodeInput:
    node_id: str

    amount_sats: Optional[int]

    funding_address: Optional[str]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "fund_node_input_node_id": self.node_id,
            "fund_node_input_amount_sats": self.amount_sats,
            "fund_node_input_funding_address": self.funding_address,
        }


def from_json(obj: Mapping[str, Any]) -> FundNodeInput:
    return FundNodeInput(
        node_id=obj["fund_node_input_node_id"],
        amount_sats=obj["fund_node_input_amount_sats"],
        funding_address=obj["fund_node_input_funding_address"],
    )
