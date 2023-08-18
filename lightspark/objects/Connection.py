# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass

from lightspark.requests.requester import Requester

from .PageInfo import PageInfo


@dataclass
class Connection:
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""
    typename: str


FRAGMENT = """
fragment ConnectionFragment on Connection {
    __typename
    ... on AccountToApiTokensConnection {
        __typename
        account_to_api_tokens_connection_count: count
        account_to_api_tokens_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        account_to_api_tokens_connection_entities: entities {
            id
        }
    }
    ... on AccountToNodesConnection {
        __typename
        account_to_nodes_connection_count: count
        account_to_nodes_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        account_to_nodes_connection_purpose: purpose
        account_to_nodes_connection_entities: entities {
            id
        }
    }
    ... on AccountToPaymentRequestsConnection {
        __typename
        account_to_payment_requests_connection_count: count
        account_to_payment_requests_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        account_to_payment_requests_connection_entities: entities {
            id
        }
    }
    ... on AccountToTransactionsConnection {
        __typename
        account_to_transactions_connection_count: count
        account_to_transactions_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
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
        account_to_transactions_connection_total_amount_transacted: total_amount_transacted {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        account_to_transactions_connection_entities: entities {
            id
        }
    }
    ... on AccountToWalletsConnection {
        __typename
        account_to_wallets_connection_count: count
        account_to_wallets_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        account_to_wallets_connection_entities: entities {
            id
        }
    }
    ... on IncomingPaymentToAttemptsConnection {
        __typename
        incoming_payment_to_attempts_connection_count: count
        incoming_payment_to_attempts_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        incoming_payment_to_attempts_connection_entities: entities {
            id
        }
    }
    ... on LightsparkNodeToChannelsConnection {
        __typename
        lightspark_node_to_channels_connection_count: count
        lightspark_node_to_channels_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        lightspark_node_to_channels_connection_entities: entities {
            id
        }
    }
    ... on OutgoingPaymentAttemptToHopsConnection {
        __typename
        outgoing_payment_attempt_to_hops_connection_count: count
        outgoing_payment_attempt_to_hops_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        outgoing_payment_attempt_to_hops_connection_entities: entities {
            id
        }
    }
    ... on OutgoingPaymentToAttemptsConnection {
        __typename
        outgoing_payment_to_attempts_connection_count: count
        outgoing_payment_to_attempts_connection_page_info: page_info {
            __typename
            page_info_has_next_page: has_next_page
            page_info_has_previous_page: has_previous_page
            page_info_start_cursor: start_cursor
            page_info_end_cursor: end_cursor
        }
        outgoing_payment_to_attempts_connection_entities: entities {
            id
        }
    }
    ... on WalletToPaymentRequestsConnection {
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
            id
        }
    }
    ... on WalletToTransactionsConnection {
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
            id
        }
    }
}
"""
