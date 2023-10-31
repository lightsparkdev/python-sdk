# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment

OUTGOING_PAYMENTS_FOR_INVOICE_QUERY = f"""
query OutgoingPaymentsForInvoice(
    $encoded_invoice: String!,
    $transaction_statuses: [TransactionStatus!] = null
) {{
    outgoing_payments_for_invoice(input: {{
        encoded_invoice: $encoded_invoice,
        statuses: $transaction_statuses
    }}) {{
        payments {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
"""
