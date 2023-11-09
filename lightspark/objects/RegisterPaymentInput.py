# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.objects.ComplianceProvider import ComplianceProvider
from lightspark.objects.PaymentDirection import PaymentDirection
from lightspark.utils.enums import parse_enum

from .ComplianceProvider import ComplianceProvider
from .PaymentDirection import PaymentDirection


@dataclass
class RegisterPaymentInput:
    provider: ComplianceProvider
    """The compliance provider that is going to screen the node. You need to be a customer of the selected provider and store the API key on the Lightspark account setting page."""

    payment_id: str
    """The Lightspark ID of the lightning payment you want to register. It can be the id of either an OutgoingPayment or an IncomingPayment."""

    node_pubkey: str
    """The public key of the counterparty lightning node, which would be the public key of the recipient node if it is to register an outgoing payment, or the public key of the sender node if it is to register an incoming payment."""

    direction: PaymentDirection
    """Indicates whether this payment is an OutgoingPayment or an IncomingPayment."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "register_payment_input_provider": self.provider.value,
            "register_payment_input_payment_id": self.payment_id,
            "register_payment_input_node_pubkey": self.node_pubkey,
            "register_payment_input_direction": self.direction.value,
        }


def from_json(obj: Mapping[str, Any]) -> RegisterPaymentInput:
    return RegisterPaymentInput(
        provider=parse_enum(ComplianceProvider, obj["register_payment_input_provider"]),
        payment_id=obj["register_payment_input_payment_id"],
        node_pubkey=obj["register_payment_input_node_pubkey"],
        direction=parse_enum(PaymentDirection, obj["register_payment_input_direction"]),
    )
