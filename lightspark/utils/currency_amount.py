# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.exceptions import LightsparkException
from lightspark.objects.CurrencyAmount import CurrencyAmount, CurrencyUnit


def amount_as_msats(currency_amount: CurrencyAmount) -> int:
    if currency_amount.original_unit == CurrencyUnit.MILLISATOSHI:
        return currency_amount.original_value
    if currency_amount.original_unit == CurrencyUnit.SATOSHI:
        return currency_amount.original_value * 1_000
    if currency_amount.original_unit == CurrencyUnit.BITCOIN:
        return currency_amount.original_value * 100_000_000_000
    if currency_amount.original_unit == CurrencyUnit.MICROBITCOIN:
        return currency_amount.original_value * 100_000
    if currency_amount.original_unit == CurrencyUnit.MILLIBITCOIN:
        return currency_amount.original_value * 100_000_000
    if currency_amount.original_unit == CurrencyUnit.NANOBITCOIN:
        return currency_amount.original_value * 100

    raise LightsparkException(
        "UNEXPECTED_CURRENCY",
        f"Expect a bitcoin currency unit, but found {currency_amount.original_unit.name}",
    )
