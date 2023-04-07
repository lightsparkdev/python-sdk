# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.CurrencyAmount import CurrencyAmount
from lightspark.objects.CurrencyUnit import CurrencyUnit
from lightspark.requests.requester import Requester


class TestCurrencyAmount:
    def test_convert_to(self) -> None:
        requester = Requester(api_token_client_id="", api_token_client_secret="")

        amount = currency_amount_sats(requester=requester, value=42).convert_to(
            CurrencyUnit.MILLISATOSHI
        )
        assert amount.preferred_currency_unit == CurrencyUnit.MILLISATOSHI
        assert amount.preferred_currency_value_approx == 42000

        amount = currency_amount_sats(requester=requester, value=42).convert_to(
            CurrencyUnit.SATOSHI
        )
        assert amount.preferred_currency_unit == CurrencyUnit.SATOSHI
        assert amount.preferred_currency_value_approx == 42

        amount = currency_amount_sats(requester=requester, value=42).convert_to(
            CurrencyUnit.BITCOIN
        )
        assert amount.preferred_currency_unit == CurrencyUnit.BITCOIN
        assert amount.preferred_currency_value_approx == 0

        amount = currency_amount_sats(requester=requester, value=4242424242).convert_to(
            CurrencyUnit.BITCOIN
        )
        assert amount.preferred_currency_unit == CurrencyUnit.BITCOIN
        assert amount.preferred_currency_value_approx == 42

        amount = currency_amount_sats(requester=requester, value=4252424242).convert_to(
            CurrencyUnit.BITCOIN
        )
        assert amount.preferred_currency_unit == CurrencyUnit.BITCOIN
        assert amount.preferred_currency_value_approx == 43

        amount = currency_amount_sats(requester=requester, value=42).convert_to(
            CurrencyUnit.MICROBITCOIN
        )
        assert amount.preferred_currency_unit == CurrencyUnit.MICROBITCOIN
        assert amount.preferred_currency_value_approx == 0


def currency_amount_sats(requester: Requester, value: int) -> CurrencyAmount:
    return CurrencyAmount(
        requester=requester,
        original_value=value,
        original_unit=CurrencyUnit.SATOSHI,
        preferred_currency_value_rounded=value,
        preferred_currency_value_approx=float(value),
        preferred_currency_unit=CurrencyUnit.SATOSHI,
    )
