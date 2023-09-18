# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment

CREATE_INVOICE_MUTATION = f"""
mutation CreateInvoice(
    $node_id: ID!
    $amount_msats: Long!
    $memo: String
    $invoice_type: InvoiceType
    $expiry_secs: Int
) {{
    create_invoice(input: {{
        node_id: $node_id
        amount_msats: $amount_msats
        memo: $memo
        invoice_type: $invoice_type
        expiry_secs: $expiry_secs
    }}) {{
        invoice {{
            ...InvoiceFragment
        }}
    }}
}}

{InvoiceFragment}
"""
