# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class WithdrawalFeeEstimateOutput:

    requester: Requester

    fee_estimate: CurrencyAmount
    """The estimated fee for the withdrawal."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "withdrawal_fee_estimate_output_fee_estimate": self.fee_estimate.to_json(),
        }


FRAGMENT = """
fragment WithdrawalFeeEstimateOutputFragment on WithdrawalFeeEstimateOutput {
    __typename
    withdrawal_fee_estimate_output_fee_estimate: fee_estimate {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> WithdrawalFeeEstimateOutput:
    return WithdrawalFeeEstimateOutput(
        requester=requester,
        fee_estimate=CurrencyAmount_from_json(
            requester, obj["withdrawal_fee_estimate_output_fee_estimate"]
        ),
    )
