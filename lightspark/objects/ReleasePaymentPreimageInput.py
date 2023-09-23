# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class ReleasePaymentPreimageInput:
    invoice_id: str
    """The invoice the preimage belongs to."""

    payment_preimage: str
    """The preimage to release."""


def from_json(obj: Mapping[str, Any]) -> ReleasePaymentPreimageInput:
    return ReleasePaymentPreimageInput(
        invoice_id=obj["release_payment_preimage_input_invoice_id"],
        payment_preimage=obj["release_payment_preimage_input_payment_preimage"],
    )
