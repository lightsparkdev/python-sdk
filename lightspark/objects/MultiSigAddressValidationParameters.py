# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class MultiSigAddressValidationParameters:
    requester: Requester

    counterparty_funding_pubkey: str
    """The counterparty funding public key used to create the 2-of-2 multisig for the address."""

    funding_pubkey_derivation_path: str
    """The derivation path used to derive the funding public key for the 2-of-2 multisig address."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "multi_sig_address_validation_parameters_counterparty_funding_pubkey": self.counterparty_funding_pubkey,
            "multi_sig_address_validation_parameters_funding_pubkey_derivation_path": self.funding_pubkey_derivation_path,
        }


FRAGMENT = """
fragment MultiSigAddressValidationParametersFragment on MultiSigAddressValidationParameters {
    __typename
    multi_sig_address_validation_parameters_counterparty_funding_pubkey: counterparty_funding_pubkey
    multi_sig_address_validation_parameters_funding_pubkey_derivation_path: funding_pubkey_derivation_path
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> MultiSigAddressValidationParameters:
    return MultiSigAddressValidationParameters(
        requester=requester,
        counterparty_funding_pubkey=obj[
            "multi_sig_address_validation_parameters_counterparty_funding_pubkey"
        ],
        funding_pubkey_derivation_path=obj[
            "multi_sig_address_validation_parameters_funding_pubkey_derivation_path"
        ],
    )
