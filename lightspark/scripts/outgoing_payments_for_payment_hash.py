# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment

OUTGOING_PAYMENTS_FOR_PAYMENT_HASH_QUERY = f"""
query OutgoingPaymentsForPaymentHash(
    $payment_hash: String!,
    $transaction_statuses: [TransactionStatus!] = null
) {{
    outgoing_payments_for_payment_hash(input: {{
        payment_hash: $payment_hash,
        statuses: $transaction_statuses
    }}) {{
        payments {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
"""
