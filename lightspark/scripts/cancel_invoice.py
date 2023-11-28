# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment

CANCEL_INVOICE_MUTATION = f"""
mutation CancelInvoice(
    $invoice_id: ID!
) {{
    cancel_invoice(input: {{
        invoice_id: $invoice_id
    }}) {{
        invoice {{
            ...InvoiceFragment
        }}
    }}
}}

{InvoiceFragment}
"""
