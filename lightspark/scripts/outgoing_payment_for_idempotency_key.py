# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment

OUTGOING_PAYMENT_FOR_IDEMPOTENCY_KEY_QUERY = f"""
query OutgoingPaymentForIdempotencyKey(
    $idempotency_key: String!
) {{
    outgoing_payment_for_idempotency_key(input: {{
        idempotency_key: $idempotency_key
    }}) {{
        payment {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
"""
