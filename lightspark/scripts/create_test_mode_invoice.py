# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

CREATE_TEST_MODE_INVOICE_MUTATION = """
mutation CreateTestModeInvoice(
    $local_node_id: ID!
    $amount_msats: Long!
    $memo: String
    $invoice_type: InvoiceType
) {
    create_test_mode_invoice(input: {
        local_node_id: $local_node_id
        amount_msats: $amount_msats
        memo: $memo
        invoice_type: $invoice_type
    }) {
        encoded_payment_request
    }
}
"""
