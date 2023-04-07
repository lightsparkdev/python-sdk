# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class LightningFeeEstimateOutput:
    requester: Requester

    fee_estimate: CurrencyAmount
    """The estimated fees for the payment."""


FRAGMENT = """
fragment LightningFeeEstimateOutputFragment on LightningFeeEstimateOutput {
    __typename
    lightning_fee_estimate_output_fee_estimate: fee_estimate {
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
) -> LightningFeeEstimateOutput:
    return LightningFeeEstimateOutput(
        requester=requester,
        fee_estimate=CurrencyAmount_from_json(
            requester, obj["lightning_fee_estimate_output_fee_estimate"]
        ),
    )
