# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.LightningFeeEstimateOutput import (
    FRAGMENT as LightningFeeEstimateFragment,
)

LIGHTNING_FEE_ESTIMATE_FOR_INVOICE_QUERY = f"""
query LightningFeeEstimateForInvoice(
    $node_id: ID!
    $encoded_payment_request: String!
    $amount_msats: Long
  ) {{
    lightning_fee_estimate_for_invoice(input: {{
      node_id: $node_id,
      encoded_payment_request: $encoded_payment_request,
      amount_msats: $amount_msats
    }}) {{
      ...LightningFeeEstimateOutputFragment
    }}
  }}

{LightningFeeEstimateFragment}
"""
