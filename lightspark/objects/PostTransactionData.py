# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class PostTransactionData:
    """This object represents post-transaction data that could be used to register payment for KYT."""

    requester: Requester

    utxo: str
    """The utxo of the channel over which the payment went through in the format of <transaction_hash>:<output_index>."""

    amount: CurrencyAmount
    """The amount of funds transferred in the payment."""


FRAGMENT = """
fragment PostTransactionDataFragment on PostTransactionData {
    __typename
    post_transaction_data_utxo: utxo
    post_transaction_data_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> PostTransactionData:
    return PostTransactionData(
        requester=requester,
        utxo=obj["post_transaction_data_utxo"],
        amount=CurrencyAmount_from_json(requester, obj["post_transaction_data_amount"]),
    )
