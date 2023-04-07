# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.objects.BitcoinNetwork import BitcoinNetwork
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .BitcoinNetwork import BitcoinNetwork
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Node import Node
from .Node import from_json as Node_from_json
from .PaymentRequestData import PaymentRequestData


@dataclass
class InvoiceData(PaymentRequestData):
    """This object represents the BOLT #11 invoice protocol for Lightning Payments. See https://github.com/lightning/bolts/blob/master/11-payment-encoding.md."""

    requester: Requester

    encoded_payment_request: str

    bitcoin_network: BitcoinNetwork

    payment_hash: str

    amount: CurrencyAmount

    created_at: datetime

    expires_at: datetime

    destination: Node

    memo: Optional[str]

    typename: str


FRAGMENT = """
fragment InvoiceDataFragment on InvoiceData {
    __typename
    invoice_data_encoded_payment_request: encoded_payment_request
    invoice_data_bitcoin_network: bitcoin_network
    invoice_data_payment_hash: payment_hash
    invoice_data_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    invoice_data_created_at: created_at
    invoice_data_expires_at: expires_at
    invoice_data_destination: destination {
        __typename
        ... on GraphNode {
            __typename
            graph_node_id: id
            graph_node_created_at: created_at
            graph_node_updated_at: updated_at
            graph_node_alias: alias
            graph_node_bitcoin_network: bitcoin_network
            graph_node_color: color
            graph_node_conductivity: conductivity
            graph_node_display_name: display_name
            graph_node_public_key: public_key
        }
        ... on LightsparkNode {
            __typename
            lightspark_node_id: id
            lightspark_node_created_at: created_at
            lightspark_node_updated_at: updated_at
            lightspark_node_alias: alias
            lightspark_node_bitcoin_network: bitcoin_network
            lightspark_node_color: color
            lightspark_node_conductivity: conductivity
            lightspark_node_display_name: display_name
            lightspark_node_public_key: public_key
            lightspark_node_account: account {
                id
            }
            lightspark_node_blockchain_balance: blockchain_balance {
                __typename
                blockchain_balance_total_balance: total_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                blockchain_balance_confirmed_balance: confirmed_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                blockchain_balance_unconfirmed_balance: unconfirmed_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                blockchain_balance_locked_balance: locked_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                blockchain_balance_required_reserve: required_reserve {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                blockchain_balance_available_balance: available_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
            }
            lightspark_node_encrypted_signing_private_key: encrypted_signing_private_key {
                __typename
                secret_encrypted_value: encrypted_value
                secret_cipher: cipher
            }
            lightspark_node_total_balance: total_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_total_local_balance: total_local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_local_balance: local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_purpose: purpose
            lightspark_node_remote_balance: remote_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_status: status
        }
    }
    invoice_data_memo: memo
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> InvoiceData:
    return InvoiceData(
        requester=requester,
        typename="InvoiceData",
        encoded_payment_request=obj["invoice_data_encoded_payment_request"],
        bitcoin_network=parse_enum(BitcoinNetwork, obj["invoice_data_bitcoin_network"]),
        payment_hash=obj["invoice_data_payment_hash"],
        amount=CurrencyAmount_from_json(requester, obj["invoice_data_amount"]),
        created_at=obj["invoice_data_created_at"],
        expires_at=obj["invoice_data_expires_at"],
        destination=Node_from_json(requester, obj["invoice_data_destination"]),
        memo=obj["invoice_data_memo"],
    )
