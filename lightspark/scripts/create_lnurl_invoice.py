# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment

CREATE_LNURL_INVOICE_MUTATION = f"""
mutation CreateLnurlInvoice(
    $node_id: ID!
    $amount_msats: Long!
    $metadata_hash: String!
    $expiry_secs: Int
) {{
    create_lnurl_invoice(input: {{
        node_id: $node_id
        amount_msats: $amount_msats
        metadata_hash: $metadata_hash
        expiry_secs: $expiry_secs
    }}) {{
        invoice {{
            ...InvoiceFragment
        }}
    }}
}}

{InvoiceFragment}
"""
