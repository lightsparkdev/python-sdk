
# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class PayOfferInput():
    

    node_id: str
    """The ID of the node that will be sending the payment."""

    encoded_offer: str
    """The Bech32 offer you want to pay (as defined by the BOLT12 standard)."""

    timeout_secs: int
    """The timeout in seconds that we will try to make the payment."""

    maximum_fees_msats: int
    """The maximum amount of fees that you want to pay for this payment to be sent, expressed in msats."""

    amount_msats: Optional[int]
    """The amount you will pay for this offer, expressed in msats. It should ONLY be set when the offer amount is zero."""

    idempotency_key: Optional[str]
    """An idempotency key for this payment. If provided, it will be used to create a payment with the same idempotency key. If not provided, a new idempotency key will be generated."""



    def to_json(self) -> Mapping[str, Any]:
        return {
            "pay_offer_input_node_id": self.node_id,
            "pay_offer_input_encoded_offer": self.encoded_offer,
            "pay_offer_input_timeout_secs": self.timeout_secs,
            "pay_offer_input_maximum_fees_msats": self.maximum_fees_msats,
            "pay_offer_input_amount_msats": self.amount_msats,
            "pay_offer_input_idempotency_key": self.idempotency_key,

        }






def from_json(obj: Mapping[str, Any]) -> PayOfferInput:
    return PayOfferInput(
        node_id=obj["pay_offer_input_node_id"],
        encoded_offer=obj["pay_offer_input_encoded_offer"],
        timeout_secs=obj["pay_offer_input_timeout_secs"],
        maximum_fees_msats=obj["pay_offer_input_maximum_fees_msats"],
        amount_msats=obj["pay_offer_input_amount_msats"],
        idempotency_key=obj["pay_offer_input_idempotency_key"],

        )

