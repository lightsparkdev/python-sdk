# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

FAIL_HTLCS_MUTATION = f"""
mutation FailHtlcs($invoice_id: ID!, $cancel_invoice: Boolean!) {{
	fail_htlcs(input: {{ invoice_id: $invoice_id, cancel_invoice: $cancel_invoice }}) {{
        invoice {{
            id
        }}
    }}
}}
"""
