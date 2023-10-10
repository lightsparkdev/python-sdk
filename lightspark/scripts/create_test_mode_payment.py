# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.IncomingPayment import FRAGMENT as IncomingPaymentFragment

CREATE_TEST_MODE_PAYMENT_MUTATION = f"""
mutation CreateTestModePayment(
    $local_node_id: ID!
    $encoded_invoice: String!
    $amount_msats: Long
) {{
    create_test_mode_payment(input: {{
        local_node_id: $local_node_id
        encoded_invoice: $encoded_invoice
        amount_msats: $amount_msats
    }}) {{
        incoming_payment {{
            ...IncomingPaymentFragment
        }}
    }}
}}

{IncomingPaymentFragment}
"""
