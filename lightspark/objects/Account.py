# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester

from .AccountToApiTokensConnection import AccountToApiTokensConnection
from .AccountToApiTokensConnection import (
    from_json as AccountToApiTokensConnection_from_json,
)
from .AccountToChannelsConnection import AccountToChannelsConnection
from .AccountToChannelsConnection import (
    from_json as AccountToChannelsConnection_from_json,
)
from .AccountToNodesConnection import AccountToNodesConnection
from .AccountToNodesConnection import from_json as AccountToNodesConnection_from_json
from .AccountToPaymentRequestsConnection import AccountToPaymentRequestsConnection
from .AccountToPaymentRequestsConnection import (
    from_json as AccountToPaymentRequestsConnection_from_json,
)
from .AccountToTransactionsConnection import AccountToTransactionsConnection
from .AccountToTransactionsConnection import (
    from_json as AccountToTransactionsConnection_from_json,
)
from .BitcoinNetwork import BitcoinNetwork
from .BlockchainBalance import BlockchainBalance
from .BlockchainBalance import from_json as BlockchainBalance_from_json
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .TransactionFailures import TransactionFailures
from .TransactionStatus import TransactionStatus
from .TransactionType import TransactionType


@dataclass
class Account(Entity):
    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    name: Optional[str]
    """The name of this account."""
    typename: str

    def get_api_tokens(
        self, first: Optional[int] = None
    ) -> AccountToApiTokensConnection:
        json = self.requester.execute_graphql(
            """
query FetchAccountToApiTokensConnection($entity_id: ID!, $first: Int) {
    entity(id: $entity_id) {
        ... on Account {
            api_tokens(, first: $first) {
                __typename
                account_to_api_tokens_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                account_to_api_tokens_connection_count: count
                account_to_api_tokens_connection_entities: entities {
                    __typename
                    api_token_id: id
                    api_token_created_at: created_at
                    api_token_updated_at: updated_at
                    api_token_client_id: client_id
                    api_token_name: name
                    api_token_permissions: permissions
                }
            }
        }
    }
}
            """,
            {"entity_id": self.id, "first": first},
        )
        connection = json["entity"]["api_tokens"]
        return AccountToApiTokensConnection_from_json(self.requester, connection)

    def get_blockchain_balance(
        self,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> Optional[BlockchainBalance]:
        json = self.requester.execute_graphql(
            """
query FetchAccountBlockchainBalance($entity_id: ID!, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            blockchain_balance(, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids) {
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
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["blockchain_balance"]
        return (
            BlockchainBalance_from_json(self.requester, connection)
            if connection
            else None
        )

    def get_conductivity(
        self,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> Optional[int]:
        json = self.requester.execute_graphql(
            """
query FetchAccountConductivity($entity_id: ID!, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            conductivity(, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids)
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["conductivity"]
        return connection

    def get_local_balance(
        self,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> Optional[CurrencyAmount]:
        json = self.requester.execute_graphql(
            """
query FetchAccountLocalBalance($entity_id: ID!, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            local_balance(, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids) {
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
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["local_balance"]
        return (
            CurrencyAmount_from_json(self.requester, connection) if connection else None
        )

    def get_nodes(
        self,
        first: Optional[int] = None,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> AccountToNodesConnection:
        json = self.requester.execute_graphql(
            """
query FetchAccountToNodesConnection($entity_id: ID!, $first: Int, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            nodes(, first: $first, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids) {
                __typename
                account_to_nodes_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
                }
                account_to_nodes_connection_count: count
                account_to_nodes_connection_purpose: purpose
                account_to_nodes_connection_entities: entities {
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
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "first": first,
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["nodes"]
        return AccountToNodesConnection_from_json(self.requester, connection)

    def get_remote_balance(
        self,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> Optional[CurrencyAmount]:
        json = self.requester.execute_graphql(
            """
query FetchAccountRemoteBalance($entity_id: ID!, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            remote_balance(, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids) {
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
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["remote_balance"]
        return (
            CurrencyAmount_from_json(self.requester, connection) if connection else None
        )

    def get_uptime_percentage(
        self,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
        bitcoin_networks: Optional[List[BitcoinNetwork]] = None,
        node_ids: Optional[List[str]] = None,
    ) -> Optional[int]:
        json = self.requester.execute_graphql(
            """
query FetchAccountUptimePercentage($entity_id: ID!, $after_date: DateTime, $before_date: DateTime, $bitcoin_networks: [BitcoinNetwork!], $node_ids: [ID!]) {
    entity(id: $entity_id) {
        ... on Account {
            uptime_percentage(, after_date: $after_date, before_date: $before_date, bitcoin_networks: $bitcoin_networks, node_ids: $node_ids)
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "after_date": after_date,
                "before_date": before_date,
                "bitcoin_networks": bitcoin_networks,
                "node_ids": node_ids,
            },
        )
        connection = json["entity"]["uptime_percentage"]
        return connection

    def get_channels(
        self,
        bitcoin_network: BitcoinNetwork,
        lightning_node_id: Optional[str] = None,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
        first: Optional[int] = None,
    ) -> AccountToChannelsConnection:
        json = self.requester.execute_graphql(
            """
query FetchAccountToChannelsConnection($entity_id: ID!, $bitcoin_network: BitcoinNetwork!, $lightning_node_id: ID, $after_date: DateTime, $before_date: DateTime, $first: Int) {
    entity(id: $entity_id) {
        ... on Account {
            channels(, bitcoin_network: $bitcoin_network, lightning_node_id: $lightning_node_id, after_date: $after_date, before_date: $before_date, first: $first) {
                __typename
                account_to_channels_connection_count: count
                account_to_channels_connection_entities: entities {
                    __typename
                    channel_id: id
                    channel_created_at: created_at
                    channel_updated_at: updated_at
                    channel_funding_transaction: funding_transaction {
                        id
                    }
                    channel_capacity: capacity {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_local_balance: local_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_local_unsettled_balance: local_unsettled_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_remote_balance: remote_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_remote_unsettled_balance: remote_unsettled_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_unsettled_balance: unsettled_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_total_balance: total_balance {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_status: status
                    channel_estimated_force_closure_wait_minutes: estimated_force_closure_wait_minutes
                    channel_commit_fee: commit_fee {
                        __typename
                        currency_amount_original_value: original_value
                        currency_amount_original_unit: original_unit
                        currency_amount_preferred_currency_unit: preferred_currency_unit
                        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                    }
                    channel_fees: fees {
                        __typename
                        channel_fees_base_fee: base_fee {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        channel_fees_fee_rate_per_mil: fee_rate_per_mil
                    }
                    channel_remote_node: remote_node {
                        id
                    }
                    channel_local_node: local_node {
                        id
                    }
                    channel_short_channel_id: short_channel_id
                }
            }
        }
    }
}
            """,
            {
                "entity_id": self.id,
                "bitcoin_network": bitcoin_network,
                "lightning_node_id": lightning_node_id,
                "after_date": after_date,
                "before_date": before_date,
                "first": first,
            },
        )
        connection = json["entity"]["channels"]
        return AccountToChannelsConnection_from_json(self.requester, connection)

    def get_transactions(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        types: Optional[List[TransactionType]] = None,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
        bitcoin_network: Optional[BitcoinNetwork] = None,
        lightning_node_id: Optional[str] = None,
        statuses: Optional[List[TransactionStatus]] = None,
        exclude_failures: Optional[TransactionFailures] = None,
    ) -> AccountToTransactionsConnection:
        json = self.requester.execute_graphql(
            """
query FetchAccountToTransactionsConnection($entity_id: ID!, $first: Int, $after: String, $types: [TransactionType!], $after_date: DateTime, $before_date: DateTime, $bitcoin_network: BitcoinNetwork, $lightning_node_id: ID, $statuses: [TransactionStatus!], $exclude_failures: TransactionFailures) {
    entity(id: $entity_id) {
        ... on Account {
            transactions(, first: $first, after: $after, types: $types, after_date: $after_date, before_date: $before_date, bitcoin_network: $bitcoin_network, lightning_node_id: $lightning_node_id, statuses: $statuses, exclude_failures: $exclude_failures) {
                __typename
                account_to_transactions_connection_profit_loss: profit_loss {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                account_to_transactions_connection_average_fee_earned: average_fee_earned {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                account_to_transactions_connection_count: count
                account_to_transactions_connection_total_amount_transacted: total_amount_transacted {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                account_to_transactions_connection_entities: entities {
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
                        }
                        outgoing_payment_failure_reason: failure_reason
                        outgoing_payment_failure_message: failure_message {
                            __typename
                            rich_text_text: text
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
                account_to_transactions_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
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
                "types": types,
                "after_date": after_date,
                "before_date": before_date,
                "bitcoin_network": bitcoin_network,
                "lightning_node_id": lightning_node_id,
                "statuses": statuses,
                "exclude_failures": exclude_failures,
            },
        )
        connection = json["entity"]["transactions"]
        return AccountToTransactionsConnection_from_json(self.requester, connection)

    def get_payment_requests(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None,
        bitcoin_network: Optional[BitcoinNetwork] = None,
        lightning_node_id: Optional[str] = None,
    ) -> AccountToPaymentRequestsConnection:
        json = self.requester.execute_graphql(
            """
query FetchAccountToPaymentRequestsConnection($entity_id: ID!, $first: Int, $after: String, $after_date: DateTime, $before_date: DateTime, $bitcoin_network: BitcoinNetwork, $lightning_node_id: ID) {
    entity(id: $entity_id) {
        ... on Account {
            payment_requests(, first: $first, after: $after, after_date: $after_date, before_date: $before_date, bitcoin_network: $bitcoin_network, lightning_node_id: $lightning_node_id) {
                __typename
                account_to_payment_requests_connection_count: count
                account_to_payment_requests_connection_entities: entities {
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
                account_to_payment_requests_connection_page_info: page_info {
                    __typename
                    page_info_has_next_page: has_next_page
                    page_info_has_previous_page: has_previous_page
                    page_info_start_cursor: start_cursor
                    page_info_end_cursor: end_cursor
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
                "after_date": after_date,
                "before_date": before_date,
                "bitcoin_network": bitcoin_network,
                "lightning_node_id": lightning_node_id,
            },
        )
        connection = json["entity"]["payment_requests"]
        return AccountToPaymentRequestsConnection_from_json(self.requester, connection)


FRAGMENT = """
fragment AccountFragment on Account {
    __typename
    account_id: id
    account_created_at: created_at
    account_updated_at: updated_at
    account_name: name
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Account:
    return Account(
        requester=requester,
        typename="Account",
        id=obj["account_id"],
        created_at=obj["account_created_at"],
        updated_at=obj["account_updated_at"],
        name=obj["account_name"],
    )
