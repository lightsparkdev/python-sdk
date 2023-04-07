# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class FundNodeOutput:
    requester: Requester

    amount: CurrencyAmount


FRAGMENT = """
fragment FundNodeOutputFragment on FundNodeOutput {
    __typename
    fund_node_output_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> FundNodeOutput:
    return FundNodeOutput(
        requester=requester,
        amount=CurrencyAmount_from_json(requester, obj["fund_node_output_amount"]),
    )
