
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class CreateOfferOutput():
    
    requester: Requester

    offer_id: str
    



    def to_json(self) -> Mapping[str, Any]:
        return {
            "create_offer_output_offer": { "id": self.offer_id },

        }




FRAGMENT = """
fragment CreateOfferOutputFragment on CreateOfferOutput {
    __typename
    create_offer_output_offer: offer {
        id
    }
}
"""



def from_json(requester: Requester, obj: Mapping[str, Any]) -> CreateOfferOutput:
    return CreateOfferOutput(
        requester=requester,        offer_id=obj["create_offer_output_offer"]["id"],

        )

