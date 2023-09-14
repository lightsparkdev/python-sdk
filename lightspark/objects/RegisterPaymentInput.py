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

    payment_id: str

    node_pubkey: str

    direction: PaymentDirection


def from_json(obj: Mapping[str, Any]) -> RegisterPaymentInput:
    return RegisterPaymentInput(
        provider=parse_enum(ComplianceProvider, obj["register_payment_input_provider"]),
        payment_id=obj["register_payment_input_payment_id"],
        node_pubkey=obj["register_payment_input_node_pubkey"],
        direction=parse_enum(PaymentDirection, obj["register_payment_input_direction"]),
    )
