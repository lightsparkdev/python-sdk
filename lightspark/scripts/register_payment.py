# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.LightningTransaction import (
    FRAGMENT as LightningTransactionFragment,
)

REGISTER_PAYMENT_MUTATION = f"""
mutation RegisterPayment(
    $provider: ComplianceProvider!
    $payment_id: ID!
    $node_pubkey: String!
    $direction: PaymentDirection!
) {{
    register_payment(input: {{
        provider: $provider
        payment_id: $payment_id
        node_pubkey: $node_pubkey
        direction: $direction
    }}) {{
        payment {{
            ...LightningTransactionFragment
        }}
    }}
}}

{LightningTransactionFragment}
"""
