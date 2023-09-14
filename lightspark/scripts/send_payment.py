# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment

SEND_PAYMENT_MUTATION = f"""
mutation SendPayment(
    $node_id: ID!
    $destination_public_key: String!
    $amount_msats: Long!
    $timeout_secs: Int!
    $maximum_fees_msats: Long!
) {{
    send_payment(input: {{
        node_id: $node_id
        destination_public_key: $destination_public_key
        amount_msats: $amount_msats
        timeout_secs: $timeout_secs
        maximum_fees_msats: $maximum_fees_msats
    }}) {{
        payment {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
"""
