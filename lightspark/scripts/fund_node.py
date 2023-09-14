# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.CurrencyAmount import FRAGMENT as CurrencyAmountFragment

FUND_NODE_MUTATION = f"""
mutation FundNode(
    $node_id: ID!,
    $amount_sats: Long
) {{
    fund_node(input: {{ node_id: $node_id, amount_sats: $amount_sats }}) {{
        amount {{
            ...CurrencyAmountFragment
        }}
    }}
}}

{CurrencyAmountFragment}
"""
