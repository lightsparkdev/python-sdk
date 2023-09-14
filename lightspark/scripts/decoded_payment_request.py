# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.InvoiceData import FRAGMENT as InvoiceDataFragment

DECODED_PAYMENT_REQUEST_QUERY = f"""
query DecodedPaymentRequest(
    $encoded_payment_request: String!
) {{
    decoded_payment_request(encoded_payment_request: $encoded_payment_request) {{
        __typename
        ... on InvoiceData {{
            ...InvoiceDataFragment
        }}
    }}
}}

{InvoiceDataFragment}
"""
