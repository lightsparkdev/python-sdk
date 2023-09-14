# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.FeeEstimate import FRAGMENT as FeeEstimateFragment

BITCOIN_FEE_ESTIMATE_QUERY = f"""
query BitcoinFeeEstimate(
    $bitcoin_network: BitcoinNetwork!
) {{
    bitcoin_fee_estimate(network: $bitcoin_network) {{
        ...FeeEstimateFragment
    }}
}}

{FeeEstimateFragment}
"""
