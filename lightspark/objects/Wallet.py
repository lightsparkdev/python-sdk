# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .Balances import Balances
from .Balances import from_json as Balances_from_json
from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity


@dataclass
class Wallet(Entity):
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
    typename: str

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
    )
