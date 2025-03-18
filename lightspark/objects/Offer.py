
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity


@dataclass
class Offer(Entity):
    """This object represents a BOLT #12 offer (https://github.com/lightning/bolts/blob/master/12-offer-encoding.md) created by a Lightspark Node."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    data_id: str
    """The details of the offer."""

    encoded_offer: str
    """The BOLT12 encoded offer. Starts with 'lno'."""

    amount: Optional[CurrencyAmount]
    """The amount of the offer. If null, the payer chooses the amount."""

    description: Optional[str]
    """The description of the offer."""
    typename: str


    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "Offer",
            "offer_id": self.id,
            "offer_created_at": self.created_at.isoformat(),
            "offer_updated_at": self.updated_at.isoformat(),
            "offer_data": { "id": self.data_id },
            "offer_encoded_offer": self.encoded_offer,
            "offer_amount": self.amount.to_json() if self.amount else None,
            "offer_description": self.description,

        }




FRAGMENT = """
fragment OfferFragment on Offer {
    __typename
    offer_id: id
    offer_created_at: created_at
    offer_updated_at: updated_at
    offer_data: data {
        id
    }
    offer_encoded_offer: encoded_offer
    offer_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    offer_description: description
}
"""



def from_json(requester: Requester, obj: Mapping[str, Any]) -> Offer:
    return Offer(
        requester=requester,        typename="Offer",        id=obj["offer_id"],
        created_at=datetime.fromisoformat(obj["offer_created_at"]),
        updated_at=datetime.fromisoformat(obj["offer_updated_at"]),
        data_id=obj["offer_data"]["id"],
        encoded_offer=obj["offer_encoded_offer"],
        amount=CurrencyAmount_from_json(requester, obj["offer_amount"]) if obj["offer_amount"] else None,
        description=obj["offer_description"],

        )

