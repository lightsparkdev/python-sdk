# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.LightningFeeEstimateOutput import (
    FRAGMENT as LightningFeeEstimateFragment,
)

LIGHTNING_FEE_ESTIMATE_FOR_NODE_QUERY = f"""
query LightningFeeEstimateForNode(
    $node_id: ID!
    $destination_node_public_key: String!
    $amount_msats: Long!
  ) {{
    lightning_fee_estimate_for_node(input: {{
      node_id: $node_id,
      destination_node_public_key: $destination_node_public_key,
      amount_msats: $amount_msats
    }}) {{
      ...LightningFeeEstimateOutputFragment
    }}
  }}

{LightningFeeEstimateFragment}
"""
