# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester

from .Connection import Connection
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .PageInfo import PageInfo
from .PageInfo import from_json as PageInfo_from_json
from .Transaction import Transaction
from .Transaction import from_json as Transaction_from_json


@dataclass
class AccountToTransactionsConnection(Connection):
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    page_info: PageInfo
    """An object that holds pagination information about the objects in this connection."""

    profit_loss: Optional[CurrencyAmount]
    """Profit (or loss) generated by the transactions in this connection, with the set of filters and constraints provided."""

    average_fee_earned: Optional[CurrencyAmount]
    """Average fee earned for the transactions in this connection, with the set of filters and constraints provided."""

    total_amount_transacted: Optional[CurrencyAmount]
    """Total amount transacted by the transactions in this connection, with the set of filters and constraints provided."""

    entities: List[Transaction]
    """The transactions for the current page of this connection."""
    typename: str


FRAGMENT = """
fragment AccountToTransactionsConnectionFragment on AccountToTransactionsConnection {
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
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> AccountToTransactionsConnection:
    return AccountToTransactionsConnection(
        requester=requester,
        typename="AccountToTransactionsConnection",
        count=obj["account_to_transactions_connection_count"],
        page_info=PageInfo_from_json(
            requester, obj["account_to_transactions_connection_page_info"]
        ),
        profit_loss=CurrencyAmount_from_json(
            requester, obj["account_to_transactions_connection_profit_loss"]
        )
        if obj["account_to_transactions_connection_profit_loss"]
        else None,
        average_fee_earned=CurrencyAmount_from_json(
            requester, obj["account_to_transactions_connection_average_fee_earned"]
        )
        if obj["account_to_transactions_connection_average_fee_earned"]
        else None,
        total_amount_transacted=CurrencyAmount_from_json(
            requester, obj["account_to_transactions_connection_total_amount_transacted"]
        )
        if obj["account_to_transactions_connection_total_amount_transacted"]
        else None,
        entities=list(
            map(
                lambda e: Transaction_from_json(requester, e),
                obj["account_to_transactions_connection_entities"],
            )
        ),
    )
