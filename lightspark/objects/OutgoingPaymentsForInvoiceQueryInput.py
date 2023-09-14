# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.utils.enums import parse_optional_list_of_enums

from .TransactionStatus import TransactionStatus


@dataclass
class OutgoingPaymentsForInvoiceQueryInput:
    encoded_invoice: str
    """The encoded invoice that the outgoing payments paid to."""

    statuses: Optional[List[TransactionStatus]]
    """An optional filter to only query outgoing payments of given statuses."""


def from_json(obj: Mapping[str, Any]) -> OutgoingPaymentsForInvoiceQueryInput:
    return OutgoingPaymentsForInvoiceQueryInput(
        encoded_invoice=obj[
            "outgoing_payments_for_invoice_query_input_encoded_invoice"
        ],
        statuses=parse_optional_list_of_enums(
            TransactionStatus, obj["outgoing_payments_for_invoice_query_input_statuses"]
        ),
    )
