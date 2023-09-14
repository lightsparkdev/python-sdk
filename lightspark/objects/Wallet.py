# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.objects.WalletStatus import WalletStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .Balances import Balances
from .Balances import from_json as Balances_from_json
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .LightsparkNodeOwner import LightsparkNodeOwner
from .TransactionStatus import TransactionStatus
from .TransactionType import TransactionType
from .WalletStatus import WalletStatus
from .WalletToPaymentRequestsConnection import WalletToPaymentRequestsConnection
from .WalletToPaymentRequestsConnection import (
    from_json as WalletToPaymentRequestsConnection_from_json,
)
from .WalletToTransactionsConnection import WalletToTransactionsConnection
from .WalletToTransactionsConnection import (
    from_json as WalletToTransactionsConnection_from_json,
)


@dataclass
class Wallet(LightsparkNodeOwner, Entity):
    """This object represents a Lightspark Wallet, tied to your Lightspark account. Wallets can be used to send or receive funds over the Lightning Network. You can retrieve this object to receive information about a specific wallet tied to your Lightspark account."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    last_login_at: Optional[datetime]
    """The date and time when the wallet user last logged in."""

    balances: Optional[Balances]
    """The balances that describe the funds in this wallet."""

    third_party_identifier: str
    """The unique identifier of this wallet, as provided by the Lightspark Customer during login."""

    account_id: Optional[str]
    """The account this wallet belongs to."""

    status: WalletStatus
    """The status of this wallet."""
    typename: str

    def get_transactions(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        created_after_date: Optional[datetime] = None,
        created_before_date: Optional[datetime] = None,
        statuses: Optional[List[TransactionStatus]] = None,
        types: Optional[List[TransactionType]] = None,
    ) -> WalletToTransactionsConnection:
        json = self.requester.execute_graphql(
            """
query FetchWalletToTransactionsConnection($entity_id: ID!, $first: Int, $after: ID, $created_after_date: DateTime, $created_before_date: DateTime, $statuses: [TransactionStatus!], $types: [TransactionType!]) {
    entity(id: $entity_id) {
        ... on Wallet {
            transactions(, first: $first, after: $after, created_after_date: $created_after_date, created_before_date: $created_before_date, statuses: $statuses, types: $types) {
                __typename
                wallet_to_transactions_connection_count: count
                wallet_to_transactions_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                wallet_to_transactions_connection_entities: entities {
                    __typename
                    ... on ChannelClosingTransaction {
                        __typename
                        channel_closing_transaction_id: id
                        channel_closing_transaction_created_at: created_at
                        channel_closing_transaction_updated_at: updated_at
                        channel_closing_transaction_status: status
                        channel_closing_transaction_resolved_at: resolved_at
                        channel_closing_transaction_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        channel_closing_transaction_transaction_hash: transaction_hash
                        channel_closing_transaction_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        channel_closing_transaction_block_hash: block_hash
                        channel_closing_transaction_block_height: block_height
                        channel_closing_transaction_destination_addresses: destination_addresses
                        channel_closing_transaction_num_confirmations: num_confirmations
                        channel_closing_transaction_channel: channel {
                            id
                        }
                    }
                    ... on ChannelOpeningTransaction {
                        __typename
                        channel_opening_transaction_id: id
                        channel_opening_transaction_created_at: created_at
                        channel_opening_transaction_updated_at: updated_at
                        channel_opening_transaction_status: status
                        channel_opening_transaction_resolved_at: resolved_at
                        channel_opening_transaction_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        channel_opening_transaction_transaction_hash: transaction_hash
                        channel_opening_transaction_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        channel_opening_transaction_block_hash: block_hash
                        channel_opening_transaction_block_height: block_height
                        channel_opening_transaction_destination_addresses: destination_addresses
                        channel_opening_transaction_num_confirmations: num_confirmations
                        channel_opening_transaction_channel: channel {
                            id
                        }
                    }
                    ... on Deposit {
                        __typename
                        deposit_id: id
                        deposit_created_at: created_at
                        deposit_updated_at: updated_at
                        deposit_status: status
                        deposit_resolved_at: resolved_at
                        deposit_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        deposit_transaction_hash: transaction_hash
                        deposit_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        deposit_block_hash: block_hash
                        deposit_block_height: block_height
                        deposit_destination_addresses: destination_addresses
                        deposit_num_confirmations: num_confirmations
                        deposit_destination: destination {
                            id
                        }
                    }
                    ... on IncomingPayment {
                        __typename
                        incoming_payment_id: id
                        incoming_payment_created_at: created_at
                        incoming_payment_updated_at: updated_at
                        incoming_payment_status: status
                        incoming_payment_resolved_at: resolved_at
                        incoming_payment_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        incoming_payment_transaction_hash: transaction_hash
                        incoming_payment_origin: origin {
                            id
                        }
                        incoming_payment_destination: destination {
                            id
                        }
                        incoming_payment_payment_request: payment_request {
                            id
                        }
                        incoming_payment_uma_post_transaction_data: uma_post_transaction_data {
                            __typename
                            post_transaction_data_utxo: utxo
                            post_transaction_data_amount: amount {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                        }
                    }
                    ... on OutgoingPayment {
                        __typename
                        outgoing_payment_id: id
                        outgoing_payment_created_at: created_at
                        outgoing_payment_updated_at: updated_at
                        outgoing_payment_status: status
                        outgoing_payment_resolved_at: resolved_at
                        outgoing_payment_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        outgoing_payment_transaction_hash: transaction_hash
                        outgoing_payment_origin: origin {
                            id
                        }
                        outgoing_payment_destination: destination {
                            id
                        }
                        outgoing_payment_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        outgoing_payment_payment_request_data: payment_request_data {
                            __typename
                            ... on InvoiceData {
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
                                        lightspark_node_owner: owner {
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
                                        lightspark_node_uma_prescreening_utxos: uma_prescreening_utxos
                                    }
                                }
                            }
                        }
                        outgoing_payment_failure_reason: failure_reason
                        outgoing_payment_failure_message: failure_message {
                            __typename
                            rich_text_text: text
                        }
                        outgoing_payment_uma_post_transaction_data: uma_post_transaction_data {
                            __typename
                            post_transaction_data_utxo: utxo
                            post_transaction_data_amount: amount {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                        }
                    }
                    ... on RoutingTransaction {
                        __typename
                        routing_transaction_id: id
                        routing_transaction_created_at: created_at
                        routing_transaction_updated_at: updated_at
                        routing_transaction_status: status
                        routing_transaction_resolved_at: resolved_at
                        routing_transaction_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        routing_transaction_transaction_hash: transaction_hash
                        routing_transaction_incoming_channel: incoming_channel {
                            id
                        }
                        routing_transaction_outgoing_channel: outgoing_channel {
                            id
                        }
                        routing_transaction_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        routing_transaction_failure_message: failure_message {
                            __typename
                            rich_text_text: text
                        }
                        routing_transaction_failure_reason: failure_reason
                    }
                    ... on Withdrawal {
                        __typename
                        withdrawal_id: id
                        withdrawal_created_at: created_at
                        withdrawal_updated_at: updated_at
                        withdrawal_status: status
                        withdrawal_resolved_at: resolved_at
                        withdrawal_amount: amount {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        withdrawal_transaction_hash: transaction_hash
                        withdrawal_fees: fees {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        withdrawal_block_hash: block_hash
                        withdrawal_block_height: block_height
                        withdrawal_destination_addresses: destination_addresses
                        withdrawal_num_confirmations: num_confirmations
                        withdrawal_origin: origin {
                            id
                        }
                    }
                }
            }
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "first": first,
                "after": after,
                "created_after_date": created_after_date,
                "created_before_date": created_before_date,
                "statuses": statuses,
                "types": types,
            },
        )
        connection = json["entity"]["transactions"]
        return WalletToTransactionsConnection_from_json(self.requester, connection)

    def get_payment_requests(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        created_after_date: Optional[datetime] = None,
        created_before_date: Optional[datetime] = None,
    ) -> WalletToPaymentRequestsConnection:
        json = self.requester.execute_graphql(
            """
query FetchWalletToPaymentRequestsConnection($entity_id: ID!, $first: Int, $after: ID, $created_after_date: DateTime, $created_before_date: DateTime) {
    entity(id: $entity_id) {
        ... on Wallet {
            payment_requests(, first: $first, after: $after, created_after_date: $created_after_date, created_before_date: $created_before_date) {
                __typename
                wallet_to_payment_requests_connection_count: count
                wallet_to_payment_requests_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                wallet_to_payment_requests_connection_entities: entities {
                    __typename
                    ... on Invoice {
                        __typename
                        invoice_id: id
                        invoice_created_at: created_at
                        invoice_updated_at: updated_at
                        invoice_data: data {
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
                                    lightspark_node_owner: owner {
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
                                    lightspark_node_uma_prescreening_utxos: uma_prescreening_utxos
                                }
                            }
                        }
                        invoice_status: status
                        invoice_amount_paid: amount_paid {
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
    }
}
            """,
            {
                "entity_id": self.id,
                "first": first,
                "after": after,
                "created_after_date": created_after_date,
                "created_before_date": created_before_date,
            },
        )
        connection = json["entity"]["payment_requests"]
        return WalletToPaymentRequestsConnection_from_json(self.requester, connection)

    def get_total_amount_received(
        self,
        created_after_date: Optional[datetime] = None,
        created_before_date: Optional[datetime] = None,
    ) -> CurrencyAmount:
        json = self.requester.execute_graphql(
            """
query FetchWalletTotalAmountReceived($entity_id: ID!, $created_after_date: DateTime, $created_before_date: DateTime) {
    entity(id: $entity_id) {
        ... on Wallet {
            total_amount_received(, created_after_date: $created_after_date, created_before_date: $created_before_date) {
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
            """,
            {
                "entity_id": self.id,
                "created_after_date": created_after_date,
                "created_before_date": created_before_date,
            },
        )
        connection = json["entity"]["total_amount_received"]
        return CurrencyAmount_from_json(self.requester, connection)

    def get_total_amount_sent(
        self,
        created_after_date: Optional[datetime] = None,
        created_before_date: Optional[datetime] = None,
    ) -> CurrencyAmount:
        json = self.requester.execute_graphql(
            """
query FetchWalletTotalAmountSent($entity_id: ID!, $created_after_date: DateTime, $created_before_date: DateTime) {
    entity(id: $entity_id) {
        ... on Wallet {
            total_amount_sent(, created_after_date: $created_after_date, created_before_date: $created_before_date) {
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
            """,
            {
                "entity_id": self.id,
                "created_after_date": created_after_date,
                "created_before_date": created_before_date,
            },
        )
        connection = json["entity"]["total_amount_sent"]
        return CurrencyAmount_from_json(self.requester, connection)


FRAGMENT = """
fragment WalletFragment on Wallet {
    __typename
    wallet_id: id
    wallet_created_at: created_at
    wallet_updated_at: updated_at
    wallet_last_login_at: last_login_at
    wallet_balances: balances {
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
    wallet_third_party_identifier: third_party_identifier
    wallet_account: account {
        id
    }
    wallet_status: status
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Wallet:
    return Wallet(
        requester=requester,
        typename="Wallet",
        id=obj["wallet_id"],
        created_at=obj["wallet_created_at"],
        updated_at=obj["wallet_updated_at"],
        last_login_at=obj["wallet_last_login_at"],
        balances=Balances_from_json(requester, obj["wallet_balances"])
        if obj["wallet_balances"]
        else None,
        third_party_identifier=obj["wallet_third_party_identifier"],
        account_id=obj["wallet_account"]["id"] if obj["wallet_account"] else None,
        status=parse_enum(WalletStatus, obj["wallet_status"]),
    )
