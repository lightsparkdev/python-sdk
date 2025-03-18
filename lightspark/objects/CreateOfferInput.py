
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class CreateOfferInput():
    

    node_id: str
    """The node from which to create the offer."""

    amount_msats: Optional[int]
    """The amount for which the offer should be created, in millisatoshis. Setting the amount to 0 will allow the payer to specify an amount."""

    description: Optional[str]
    """A short description of the offer."""



    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_offer_input_node_id": self.node_id,
            "create_offer_input_amount_msats": self.amount_msats,
            "create_offer_input_description": self.description,

        }






def from_json(obj: Mapping[str, Any]) -> CreateOfferInput:
    return CreateOfferInput(
        node_id=obj["create_offer_input_node_id"],
        amount_msats=obj["create_offer_input_amount_msats"],
        description=obj["create_offer_input_description"],

        )

