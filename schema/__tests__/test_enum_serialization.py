# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.CurrencyAmount import CurrencyAmount
from lightspark.objects.CurrencyUnit import CurrencyUnit
from lightspark.requests.requester import Requester
from lightspark.objects.TransactionFailures import (
    from_json as TransactionFailures_fromJson,
)
from lightspark.objects.PaymentFailureReason import PaymentFailureReason
from lightspark.objects.RoutingTransactionFailureReason import (
    RoutingTransactionFailureReason,
)
from lightspark.objects import CreateInvoiceInput
from lightspark.objects.InvoiceType import InvoiceType
from lightspark.objects import NodeAddress
from lightspark.objects.NodeAddressType import NodeAddressType


class TestEnumSerialization:
    def test_list_of_enums_serializing(self) -> None:
        serialized_failures = {
            "transaction_failures_payment_failures": [
                "INSUFFICIENT_BALANCE",
                "ON_FIRE",
            ],
            "transaction_failures_routing_transaction_failures": [
                "OUTGOING_LINK_FAILURE",
                "INCOMING_LINK_FAILURE",
                "ON_FIRE",
            ],
        }

        failures = TransactionFailures_fromJson(serialized_failures)
        assert failures.payment_failures == [
            PaymentFailureReason.INSUFFICIENT_BALANCE,
            PaymentFailureReason.___FUTURE_VALUE___,
        ]
        assert failures.routing_transaction_failures == [
            RoutingTransactionFailureReason.OUTGOING_LINK_FAILURE,
            RoutingTransactionFailureReason.INCOMING_LINK_FAILURE,
            RoutingTransactionFailureReason.___FUTURE_VALUE___,
        ]

        serialized_failures = {
            "transaction_failures_payment_failures": [],
            "transaction_failures_routing_transaction_failures": None,
        }

        failures = TransactionFailures_fromJson(serialized_failures)
        assert failures.payment_failures == None
        assert failures.routing_transaction_failures is None

    def test_enum_deserializing(self) -> None:
        serialized_address = {
            "node_address_address": "192.168.1.1",
            "node_address_type": "IPV4",
        }

        node_address = NodeAddress.from_json(Requester("", ""), serialized_address)
        assert node_address.type == NodeAddressType.IPV4

        serialized_address = {
            "node_address_address": "192.16fffkh8.1.1",
            "node_address_type": "ON_FIRE",
        }

        node_address = NodeAddress.from_json(Requester("", ""), serialized_address)
        assert node_address.type == NodeAddressType.___FUTURE_VALUE___

    def test_nullable_enum_serializing(self) -> None:
        serialzed_invoice_input = {
            "create_invoice_input_node_id": "node_id",
            "create_invoice_input_amount_msats": "100000",
            "create_invoice_input_memo": "memo",
            "create_invoice_input_invoice_type": "AMP",
            "create_invoice_input_expiry_secs": "100",
            "create_invoice_input_payment_hash": "payment_hash",
            "create_invoice_input_preimage_nonce": "preimage_nonce",
        }

        invoice_input = CreateInvoiceInput.from_json(serialzed_invoice_input)
        assert invoice_input.invoice_type == InvoiceType.AMP

        serialzed_invoice_input = {
            "create_invoice_input_node_id": "node_id",
            "create_invoice_input_amount_msats": "100000",
            "create_invoice_input_memo": "memo",
            "create_invoice_input_invoice_type": "ON_FIRE",
            "create_invoice_input_expiry_secs": None,
            "create_invoice_input_payment_hash": None,
            "create_invoice_input_preimage_nonce": None,
        }

        invoice_input = CreateInvoiceInput.from_json(serialzed_invoice_input)
        assert invoice_input.invoice_type == InvoiceType.___FUTURE_VALUE___

        serialzed_invoice_input = {
            "create_invoice_input_node_id": "node_id",
            "create_invoice_input_amount_msats": "100000",
            "create_invoice_input_memo": "memo",
            "create_invoice_input_invoice_type": None,
            "create_invoice_input_expiry_secs": None,
            "create_invoice_input_payment_hash": None,
            "create_invoice_input_preimage_nonce": None,
        }

        invoice_input = CreateInvoiceInput.from_json(serialzed_invoice_input)
        assert invoice_input.invoice_type is None
