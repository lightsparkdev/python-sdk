# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class Balances:
    """This is an object representing the balance associated with your Lightspark account. You can retrieve this object to see your balance, which can be broken down into several different categorizations."""

    requester: Requester

    owned_balance: CurrencyAmount
    """This represents the balance that should be displayed when asked "how much do I own right now?".

It represents the amount currently owned, including things that may not be owned soon (e.g. in-flight outgoing payments, in-flight withdrawals, commit fees, etc.). It really is a snapshot of what is officially owned at this instant."""

    available_to_send_balance: CurrencyAmount
    """This represents the balance that should be displayed when asked "how much can I send on Lightning right now?".

It represents the amount currently available to be sent on the Lightning network. We remove from the balance all the funds that are temporarily locked (e.g. channel reserves)."""

    available_to_withdraw_balance: CurrencyAmount
    """This represents the balance that should be displayed when asked "how much money can I withdraw on the Bitcoin network right now?".

It represents the amount currently available to withdraw and is usually equal to the `owned_balance` but it does not include in-flight operations (which would likely succeed and therefore likely make your withdrawal fail)."""


FRAGMENT = """
fragment BalancesFragment on Balances {
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
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Balances:
    return Balances(
        requester=requester,
        owned_balance=CurrencyAmount_from_json(
            requester, obj["balances_owned_balance"]
        ),
        available_to_send_balance=CurrencyAmount_from_json(
            requester, obj["balances_available_to_send_balance"]
        ),
        available_to_withdraw_balance=CurrencyAmount_from_json(
            requester, obj["balances_available_to_withdraw_balance"]
        ),
    )
