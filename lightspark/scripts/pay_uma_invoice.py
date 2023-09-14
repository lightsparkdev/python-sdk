# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment

PAY_UMA_INVOICE_MUTATION = f"""
mutation PayUmaInvoice(
    $node_id: ID!
    $encoded_invoice: String!
    $timeout_secs: Int!
    $maximum_fees_msats: Long!
    $amount_msats: Long
) {{
    pay_uma_invoice(input: {{
        node_id: $node_id
        encoded_invoice: $encoded_invoice
        timeout_secs: $timeout_secs
        maximum_fees_msats: $maximum_fees_msats
        amount_msats: $amount_msats
    }}) {{
        payment {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
"""
