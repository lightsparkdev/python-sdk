# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

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
    """This object represents the data associated with a Bolt #11 or Bolt #12 invoice. You can retrieve this object to receive the relevant data associated with a specific invoice."""

    requester: Requester

    encoded_payment_request: str

    bitcoin_network: BitcoinNetwork

    payment_hash: str
    """The payment hash of this invoice."""

    amount: CurrencyAmount
    """The requested amount in this invoice. If it is equal to 0, the sender should choose the amount to send."""

    created_at: datetime
    """The date and time when this invoice was created."""

    expires_at: datetime
    """The date and time when this invoice will expire."""

    memo: Optional[str]
    """A short, UTF-8 encoded, description of the purpose of this invoice."""

    destination: Node
    """The lightning node that will be paid when fulfilling this invoice."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "InvoiceData",
            "invoice_data_encoded_payment_request": self.encoded_payment_request,
            "invoice_data_bitcoin_network": self.bitcoin_network.value,
            "invoice_data_payment_hash": self.payment_hash,
            "invoice_data_amount": self.amount.to_json(),
            "invoice_data_created_at": self.created_at.isoformat(),
            "invoice_data_expires_at": self.expires_at.isoformat(),
            "invoice_data_memo": self.memo,
            "invoice_data_destination": self.destination.to_json(),
        }


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
    invoice_data_memo: memo
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
        ... on LightsparkNodeWithOSK {
            __typename
            lightspark_node_with_o_s_k_id: id
            lightspark_node_with_o_s_k_created_at: created_at
            lightspark_node_with_o_s_k_updated_at: updated_at
            lightspark_node_with_o_s_k_alias: alias
            lightspark_node_with_o_s_k_bitcoin_network: bitcoin_network
            lightspark_node_with_o_s_k_color: color
            lightspark_node_with_o_s_k_conductivity: conductivity
            lightspark_node_with_o_s_k_display_name: display_name
            lightspark_node_with_o_s_k_public_key: public_key
            lightspark_node_with_o_s_k_owner: owner {
                id
            }
            lightspark_node_with_o_s_k_status: status
            lightspark_node_with_o_s_k_total_balance: total_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_o_s_k_total_local_balance: total_local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_o_s_k_local_balance: local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_o_s_k_remote_balance: remote_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_o_s_k_blockchain_balance: blockchain_balance {
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
            lightspark_node_with_o_s_k_uma_prescreening_utxos: uma_prescreening_utxos
            lightspark_node_with_o_s_k_balances: balances {
                __typename
                balances_owned_balance: owned_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                balances_available_to_send_balance: available_to_send_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                balances_available_to_withdraw_balance: available_to_withdraw_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
            }
            lightspark_node_with_o_s_k_encrypted_signing_private_key: encrypted_signing_private_key {
                __typename
                secret_encrypted_value: encrypted_value
                secret_cipher: cipher
            }
        }
        ... on LightsparkNodeWithRemoteSigning {
            __typename
            lightspark_node_with_remote_signing_id: id
            lightspark_node_with_remote_signing_created_at: created_at
            lightspark_node_with_remote_signing_updated_at: updated_at
            lightspark_node_with_remote_signing_alias: alias
            lightspark_node_with_remote_signing_bitcoin_network: bitcoin_network
            lightspark_node_with_remote_signing_color: color
            lightspark_node_with_remote_signing_conductivity: conductivity
            lightspark_node_with_remote_signing_display_name: display_name
            lightspark_node_with_remote_signing_public_key: public_key
            lightspark_node_with_remote_signing_owner: owner {
                id
            }
            lightspark_node_with_remote_signing_status: status
            lightspark_node_with_remote_signing_total_balance: total_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_remote_signing_total_local_balance: total_local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_remote_signing_local_balance: local_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_remote_signing_remote_balance: remote_balance {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
            lightspark_node_with_remote_signing_blockchain_balance: blockchain_balance {
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
            lightspark_node_with_remote_signing_uma_prescreening_utxos: uma_prescreening_utxos
            lightspark_node_with_remote_signing_balances: balances {
                __typename
                balances_owned_balance: owned_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                balances_available_to_send_balance: available_to_send_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                balances_available_to_withdraw_balance: available_to_withdraw_balance {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
            }
        }
    }
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
        created_at=datetime.fromisoformat(obj["invoice_data_created_at"]),
        expires_at=datetime.fromisoformat(obj["invoice_data_expires_at"]),
        memo=obj["invoice_data_memo"],
        destination=Node_from_json(requester, obj["invoice_data_destination"]),
    )
