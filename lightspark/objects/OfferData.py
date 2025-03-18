
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum_list

from .BitcoinNetwork import BitcoinNetwork
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity


@dataclass
class OfferData(Entity):
    """This object represents the data associated with a BOLT #12 offer. You can retrieve this object to receive the relevant data associated with a specific offer."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    amount: Optional[CurrencyAmount]
    """The requested amount in this invoice. If it is equal to 0, the sender should choose the amount to send."""

    encoded_offer: str
    """The Bech32 encoded offer."""

    bitcoin_networks: List[BitcoinNetwork]
    """The bitcoin networks supported by the offer."""

    expires_at: Optional[datetime]
    """The date and time when this invoice will expire."""
    typename: str


    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "OfferData",
            "offer_data_id": self.id,
            "offer_data_created_at": self.created_at.isoformat(),
            "offer_data_updated_at": self.updated_at.isoformat(),
            "offer_data_amount": self.amount.to_json() if self.amount else None,
            "offer_data_encoded_offer": self.encoded_offer,
            "offer_data_bitcoin_networks": [e.value for e in self.bitcoin_networks],
            "offer_data_expires_at": self.expires_at.isoformat() if self.expires_at else None,

        }




FRAGMENT = """
fragment OfferDataFragment on OfferData {
    __typename
    offer_data_id: id
    offer_data_created_at: created_at
    offer_data_updated_at: updated_at
    offer_data_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    offer_data_encoded_offer: encoded_offer
    offer_data_bitcoin_networks: bitcoin_networks
    offer_data_expires_at: expires_at
}
"""



def from_json(requester: Requester, obj: Mapping[str, Any]) -> OfferData:
    return OfferData(
        requester=requester,        typename="OfferData",        id=obj["offer_data_id"],
        created_at=datetime.fromisoformat(obj["offer_data_created_at"]),
        updated_at=datetime.fromisoformat(obj["offer_data_updated_at"]),
        amount=CurrencyAmount_from_json(requester, obj["offer_data_amount"]) if obj["offer_data_amount"] else None,
        encoded_offer=obj["offer_data_encoded_offer"],
        bitcoin_networks=parse_enum_list(BitcoinNetwork, obj["offer_data_bitcoin_networks"]),
        expires_at=datetime.fromisoformat(obj["offer_data_expires_at"]) if obj["offer_data_expires_at"] else None,

        )

