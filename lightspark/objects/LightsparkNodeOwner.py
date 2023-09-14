# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from lightspark.exceptions import LightsparkException
from lightspark.objects.WalletStatus import WalletStatus
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .Balances import from_json as Balances_from_json
from .Entity import Entity


@dataclass
class LightsparkNodeOwner(Entity):
    """This is an object representing the owner of a LightsparkNode."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""
    typename: str


FRAGMENT = """
fragment LightsparkNodeOwnerFragment on LightsparkNodeOwner {
    __typename
    ... on Account {
        __typename
        account_id: id
        account_created_at: created_at
        account_updated_at: updated_at
        account_name: name
    }
    ... on Wallet {
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
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> LightsparkNodeOwner:
    if obj["__typename"] == "Account":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Account import Account

        return Account(
            requester=requester,
            typename="Account",
            id=obj["account_id"],
            created_at=obj["account_created_at"],
            updated_at=obj["account_updated_at"],
            name=obj["account_name"],
        )
    if obj["__typename"] == "Wallet":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Wallet import Wallet

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
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface LightsparkNodeOwner corresponding to the typename={graphql_typename}",
    )
