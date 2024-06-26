# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.utils.enums import parse_optional_list_of_enums

from .TransactionStatus import TransactionStatus


@dataclass
class IncomingPaymentsForInvoiceQueryInput:
    invoice_id: str

    statuses: Optional[List[TransactionStatus]]
    """An optional filter to only query outgoing payments of given statuses."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "incoming_payments_for_invoice_query_input_invoice_id": self.invoice_id,
            "incoming_payments_for_invoice_query_input_statuses": (
                [e.value for e in self.statuses] if self.statuses else None
            ),
        }


def from_json(obj: Mapping[str, Any]) -> IncomingPaymentsForInvoiceQueryInput:
    return IncomingPaymentsForInvoiceQueryInput(
        invoice_id=obj["incoming_payments_for_invoice_query_input_invoice_id"],
        statuses=parse_optional_list_of_enums(
            TransactionStatus, obj["incoming_payments_for_invoice_query_input_statuses"]
        ),
    )
