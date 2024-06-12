# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment

INVOICE_FOR_PAYMENT_HASH_QUERY = f"""
query InvoiceForPaymentHash($payment_hash: Hash32!) {{
	invoice_for_payment_hash(input: {{
		payment_hash: $payment_hash
	}}) {{
		invoice {{
			...InvoiceFragment
		}}
	}}
}}

{InvoiceFragment}
"""
