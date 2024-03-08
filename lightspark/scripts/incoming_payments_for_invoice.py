# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.IncomingPaymentsForInvoiceQueryOutput import FRAGMENT as IncomingPaymentsForInvoiceQueryOutputFragment

INCOMING_PAYMENTS_FOR_INVOICE_QUERY = f"""
query IncomingPaymentsForInvoice(
	$invoice_id: ID!
	$transaction_statuses: [TransactionStatus!]
) {{
	incoming_payments_for_invoice(input: {{
		invoice_id: $invoice_id
		transaction_statuses: $statuses
	}}) {{
		...IncomingPaymentsForInvoiceQueryOutputFragment
	}}
}}

{IncomingPaymentsForInvoiceQueryOutputFragment}
"""
