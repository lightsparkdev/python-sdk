# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import logging
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple, Type, TypeVar

from lightspark.exceptions import LightsparkException
from lightspark.objects.Account import FRAGMENT as AccountFragment
from lightspark.objects.Account import Account
from lightspark.objects.Account import from_json as Account_from_json
from lightspark.objects.all_entities import get_entity
from lightspark.objects.ApiToken import FRAGMENT as ApiTokenFragment
from lightspark.objects.ApiToken import ApiToken
from lightspark.objects.ApiToken import from_json as ApiToken_from_json
from lightspark.objects.BitcoinNetwork import BitcoinNetwork
from lightspark.objects.CurrencyAmount import FRAGMENT as CurrencyAmountFragment
from lightspark.objects.CurrencyAmount import CurrencyAmount
from lightspark.objects.CurrencyAmount import from_json as CurrencyAmount_from_json
from lightspark.objects.Entity import Entity
from lightspark.objects.FeeEstimate import FRAGMENT as FeeEstimateFragment
from lightspark.objects.FeeEstimate import FeeEstimate
from lightspark.objects.FeeEstimate import from_json as FeeEstimate_from_json
from lightspark.objects.LightningFeeEstimateOutput import (
    FRAGMENT as LightningFeeEstimateFragment,
)
from lightspark.objects.LightningFeeEstimateOutput import (
    from_json as LightningFeeEstimateOutput_from_json,
)
from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment
from lightspark.objects.Invoice import Invoice
from lightspark.objects.Invoice import from_json as Invoice_from_json
from lightspark.objects.InvoiceData import FRAGMENT as InvoiceDataFragment
from lightspark.objects.InvoiceData import from_json as InvoiceData_from_json
from lightspark.objects.InvoiceType import InvoiceType
from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment
from lightspark.objects.OutgoingPayment import OutgoingPayment
from lightspark.objects.OutgoingPayment import from_json as OutgoingPayment_from_json
from lightspark.objects.PaymentRequestData import PaymentRequestData
from lightspark.objects.Permission import Permission
from lightspark.objects.WithdrawalMode import WithdrawalMode
from lightspark.objects.WithdrawalRequest import FRAGMENT as WithdrawalRequestFragment
from lightspark.objects.WithdrawalRequest import WithdrawalRequest
from lightspark.objects.WithdrawalRequest import (
    from_json as WithdrawalRequest_from_json,
)
from lightspark.requests.requester import Requester
from lightspark.utils.crypto import decrypt_private_key

logger = logging.getLogger("lightspark")

ENTITY = TypeVar("ENTITY", bound=Entity)


@dataclass
class LightsparkSyncClient:
    _requester: Requester
    _node_private_keys: Dict[str, bytes]

    def __init__(
        self,
        api_token_client_id: str,
        api_token_client_secret: str,
        base_url: Optional[str] = None,
        http_host: Optional[str] = None,
    ) -> None:
        self._requester = Requester(
            api_token_client_id=api_token_client_id,
            api_token_client_secret=api_token_client_secret,
            base_url=base_url,
            http_host=http_host,
        )
        self._node_private_keys = {}

    def create_api_token(
        self,
        name: str,
        transact: bool = True,
        test_mode: bool = False,
    ) -> Tuple[ApiToken, str]:
        logger.info('Creating API token "%s".', name)
        permissions = {
            (False, False): (Permission.MAINNET_VIEW,),
            (False, True): (Permission.MAINNET_VIEW, Permission.MAINNET_TRANSACT),
            (True, False): (Permission.REGTEST_VIEW,),
            (True, True): (Permission.REGTEST_VIEW, Permission.REGTEST_TRANSACT),
        }[(test_mode, transact)]

        json = self._requester.execute_graphql(
            f"""
mutation CreateApiToken(
    $name: String!
    $permissions: [Permission!]!
) {{
    create_api_token(input: {{
        name: $name
        permissions: $permissions
    }}) {{
        api_token {{
            ...ApiTokenFragment
        }}
        client_secret
    }}
}}

{ApiTokenFragment}
""",
            {"name": name, "permissions": permissions},
        )

        return (
            ApiToken_from_json(self._requester, json["create_api_token"]["api_token"]),
            json["create_api_token"]["client_secret"],
        )

    def create_invoice(
        self,
        node_id: str,
        amount_msats: int,
        memo: Optional[str] = None,
        invoice_type: Optional[InvoiceType] = None,
    ) -> Invoice:
        logger.info("Creating an invoice for node %s.", node_id)
        json = self._requester.execute_graphql(
            f"""
mutation CreateInvoice(
    $node_id: ID!
    $amount_msats: Long!
    $memo: String
    $invoice_type: InvoiceType
) {{
    create_invoice(input: {{
        node_id: $node_id
        amount_msats: $amount_msats
        memo: $memo
        invoice_type: $invoice_type
    }}) {{
        invoice {{
            ...InvoiceFragment
        }}
    }}
}}

{InvoiceFragment}
""",
            {
                "amount_msats": amount_msats,
                "node_id": node_id,
                "memo": memo,
                "invoice_type": invoice_type,
            },
        )

        return Invoice_from_json(self._requester, json["create_invoice"]["invoice"])

    def create_node_wallet_address(
        self,
        node_id: str,
    ) -> str:
        logger.info("Creating a wallet address for node %s.", node_id)
        json = self._requester.execute_graphql(
            """
mutation CreateNodeWalletAddress(
    $node_id: ID!
) {
    create_node_wallet_address(input: {
        node_id: $node_id
    }) {
        wallet_address
    }
}
""",
            {"node_id": node_id},
        )
        return json["create_node_wallet_address"]["wallet_address"]

    def delete_api_token(self, api_token_id: str) -> None:
        logger.info("Deleting API token %s.", api_token_id)
        self._requester.execute_graphql(
            """
mutation DeleteApiToken(
    $api_token_id: ID!
) {
    delete_api_token(input: {
        api_token_id: $api_token_id
    }) {
        __typename
    }
}
""",
            {"api_token_id": api_token_id},
        )

    def execute_graphql_request(
        self, document: str, variables: Optional[Mapping[str, Any]] = None
    ) -> Mapping[str, Any]:
        """This function can be used to execute a custom GraphQL request against
        the Lightspark public API. It will take care of the authentication automatically.

        To find the Lightspark API documentation, see https://docs.lightspark.com/api/graphql/2023-01-01
        To learn more about GraphQL, see https://graphql.org/learn/

        Args:
            document:
                This is the GraphQL document (query or mutation) that will be
                executed against the API.
            variables (optional):
                A dictionary representing a JSON object containing the variables
                needed to execute the query or mutation in the document. This is
                optional if your document does not use any variable.

        Returns:
            A dictionary representing the JSON response received from the API.
            This JSON object can then be used to instantiate some of the python
            objects defined in the lightspark.objects.* modules, using the `from_json`
            function defined in each module.
        """
        logger.info("Executing arbitrary GraphQL request with document=%s", document)
        return self._requester.execute_graphql(query=document, variables=variables)

    def get_current_account(
        self,
    ) -> Account:
        logger.info("Fetching current account.")
        json = self._requester.execute_graphql(
            f"""
query GetCurrentAccount {{
    current_account {{
        ...AccountFragment
    }}
}}

{AccountFragment}
""",
            {},
        )
        return Account_from_json(self._requester, json["current_account"])

    def get_decoded_payment_request(
        self, encoded_payment_request: str
    ) -> PaymentRequestData:
        logger.info(
            "Decoding payment request starting with %s...",
            encoded_payment_request[0:10],
        )
        json = self._requester.execute_graphql(
            f"""
query DecodedPaymentRequest(
    $encoded_payment_request: String!
) {{
    decoded_payment_request(encoded_payment_request: $encoded_payment_request) {{
        __typename
        ... on InvoiceData {{
            ...InvoiceDataFragment
        }}
    }}
}}

{InvoiceDataFragment}
""",
            {"encoded_payment_request": encoded_payment_request},
        )
        data = json["decoded_payment_request"]
        typename = data["__typename"]
        if typename != "InvoiceData":
            raise LightsparkException(
                "UNKNOWN_TYPE", f"Unsupported type of payment request: {typename}"
            )
        return InvoiceData_from_json(self._requester, data)

    def get_entity(
        self, entity_id: str, entity_class: Type[ENTITY]
    ) -> Optional[ENTITY]:
        logger.info(
            "Fetching entity of type %s with id %s", str(entity_class), entity_id
        )
        return get_entity(
            requester=self._requester, entity_id=entity_id, entity_class=entity_class
        )

    def get_bitcoin_fee_estimate(self, bitcoin_network: BitcoinNetwork) -> FeeEstimate:
        logger.info("Querying the fee estimate for network %s.", bitcoin_network)
        json = self._requester.execute_graphql(
            f"""
query BitcoinFeeEstimate(
    $bitcoin_network: BitcoinNetwork!
) {{
    bitcoin_fee_estimate(network: $bitcoin_network) {{
        ...FeeEstimateFragment
    }}
}}

{FeeEstimateFragment}
""",
            {"bitcoin_network": bitcoin_network},
        )
        return FeeEstimate_from_json(self._requester, json["bitcoin_fee_estimate"])

    def get_lightning_fee_estimate_for_invoice(
        self,
        node_id: str,
        encoded_payment_request: str,
        amount_msats: Optional[int] = None,
    ) -> CurrencyAmount:
        variables: Dict[str, Any] = {
            "node_id": node_id,
            "encoded_payment_request": encoded_payment_request,
        }
        if amount_msats is not None:
            variables["amount_msats"] = amount_msats
        json = self._requester.execute_graphql(
            f"""
query LightningFeeEstimateForInvoice(
    $node_id: ID!
    $encoded_payment_request: String!
    $amount_msats: Long
  ) {{
    lightning_fee_estimate_for_invoice(input: {{
      node_id: $node_id,
      encoded_payment_request: $encoded_payment_request,
      amount_msats: $amount_msats
    }}) {{
      ...LightningFeeEstimateOutputFragment
    }}
  }}

{LightningFeeEstimateFragment}
""",
            variables,
        )
        return LightningFeeEstimateOutput_from_json(
            self._requester, json["lightning_fee_estimate_for_invoice"]
        ).fee_estimate

    def get_lightning_fee_estimate_for_node(
        self,
        node_id: str,
        destination_node_public_key: str,
        amount_msats: int,
    ) -> CurrencyAmount:
        json = self._requester.execute_graphql(
            f"""
query LightningFeeEstimateForNode(
    $node_id: ID!
    $destination_node_public_key: String!
    $amount_msats: Long!
  ) {{
    lightning_fee_estimate_for_node(input: {{
      node_id: $node_id,
      destination_node_public_key: $destination_node_public_key,
      amount_msats: $amount_msats
    }}) {{
      ...LightningFeeEstimateOutputFragment
    }}
  }}

{LightningFeeEstimateFragment}
""",
            {
                "node_id": node_id,
                "destination_node_public_key": destination_node_public_key,
                "amount_msats": amount_msats,
            },
        )
        return LightningFeeEstimateOutput_from_json(
            self._requester, json["lightning_fee_estimate_for_node"]
        ).fee_estimate

    def load_node_signing_key(self, node_id: str, signing_key: bytes) -> None:
        logger.info("Loading the signing key for node %s", node_id)
        self._node_private_keys[node_id] = signing_key

    def recover_node_signing_key(self, node_id: str, node_password: str) -> bytes:
        logger.info("Recovering the signing key for node %s", node_id)
        json = self._requester.execute_graphql(
            """
query RecoverNodeSigningKey(
    $node_id: ID!
) {
    entity(id: $node_id) {
        ... on LightsparkNode {
            encrypted_signing_private_key {
                encrypted_value
                cipher
            }
        }
    }
}
""",
            {"node_id": node_id},
        )
        encrypted_key = json["entity"]["encrypted_signing_private_key"][
            "encrypted_value"
        ]
        cipher = json["entity"]["encrypted_signing_private_key"]["cipher"]

        decrypted_private_key = decrypt_private_key(
            cipher_version=cipher,
            encrypted_value=encrypted_key,
            password=node_password,
        )

        self.load_node_signing_key(node_id=node_id, signing_key=decrypted_private_key)
        return decrypted_private_key

    def pay_invoice(
        self,
        node_id: str,
        encoded_invoice: str,
        timeout_secs: int,
        maximum_fees_msats: int,
        amount_msats: Optional[int] = None,
    ) -> OutgoingPayment:
        variables = {
            "node_id": node_id,
            "encoded_invoice": encoded_invoice,
            "timeout_secs": timeout_secs,
            "maximum_fees_msats": maximum_fees_msats,
        }
        if amount_msats is not None:
            variables["amount_msats"] = amount_msats
        json = self._requester.execute_graphql(
            f"""
mutation PayInvoice(
    $node_id: ID!
    $encoded_invoice: String!
    $timeout_secs: Int!
    $maximum_fees_msats: Long!
    $amount_msats: Long
) {{
    pay_invoice(input: {{
        node_id: $node_id
        encoded_invoice: $encoded_invoice
        timeout_secs: $timeout_secs
        maximum_fees_msats: $maximum_fees_msats
        amount_msats: $amount_msats
    }}) {{
        payment {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
""",
            variables,
            self.get_signing_key(node_id),
        )
        return OutgoingPayment_from_json(
            self._requester, json["pay_invoice"]["payment"]
        )

    def send_payment(
        self,
        node_id: str,
        destination_public_key: str,
        amount_msats: int,
        timeout_secs: int,
        maximum_fees_msats: int,
    ) -> OutgoingPayment:
        json = self._requester.execute_graphql(
            f"""
mutation SendPayment(
    $node_id: ID!
    $destination_public_key: String!
    $amount_msats: Long!
    $timeout_secs: Int!
    $maximum_fees_msats: Long!
) {{
    send_payment(input: {{
        node_id: $node_id
        destination_public_key: $destination_public_key
        amount_msats: $amount_msats
        timeout_secs: $timeout_secs
        maximum_fees_msats: $maximum_fees_msats
    }}) {{
        payment {{
            ...OutgoingPaymentFragment
        }}
    }}
}}

{OutgoingPaymentFragment}
""",
            {
                "node_id": node_id,
                "destination_public_key": destination_public_key,
                "amount_msats": amount_msats,
                "timeout_secs": timeout_secs,
                "maximum_fees_msats": maximum_fees_msats,
            },
            self.get_signing_key(node_id),
        )
        return OutgoingPayment_from_json(
            self._requester, json["send_payment"]["payment"]
        )

    def get_signing_key(self, node_id: str) -> bytes:
        if node_id not in self._node_private_keys:
            raise LightsparkException(
                "SIGNING_ERROR",
                f"We did not find the signing key for node {node_id}. Please call"
                + " the `recover_node_signing_key` or `load_node_signing_key` methods.",
            )
        return self._node_private_keys[node_id]

    def fund_node(
        self,
        node_id: str,
        amount_sats: int,
    ) -> CurrencyAmount:
        """Adds funds to a Lightspark node on the REGTEST network. If the amount is not specified, 10,000,000 SATOSHI
        will be added. This API only functions for nodes created on the REGTEST network and will return an error when
        called for any non-REGTEST node.

        Args:
            node_id (str): The ID of the node to fund. Must be a REGTEST node.
            amount_sats (int): The amount of funds to add to the node in SATOSHI. If not specified, 10,000,000 SATOSHI
            will be added.

        Returns:
            CurrencyAmount: The amount of funds added to the node.
        """
        json = self._requester.execute_graphql(
            f"""
mutation FundNode(
    $node_id: ID!,
    $amount_sats: Long
) {{
    fund_node(input: {{ node_id: $node_id, amount_sats: $amount_sats }}) {{
        amount {{
            ...CurrencyAmountFragment
        }}
    }}
}}

{CurrencyAmountFragment}
""",
            {
                "node_id": node_id,
                "amount_sats": amount_sats,
            },
        )
        return CurrencyAmount_from_json(self._requester, json["fund_node"]["amount"])

    def request_withdrawal(
        self,
        node_id: str,
        amount_sats: int,
        bitcoin_address: str,
        withdrawal_mode: WithdrawalMode,
    ) -> WithdrawalRequest:
        """Withdraws funds from the account and sends it to the requested bitcoin address.

        Depending on the chosen mode, it will first take the funds from the wallet, and if applicable, close channels appropriately to recover enough funds and reopen channels with the remaining funds.
        The process is asynchronous and may take up to a few minutes. You can check the progress by polling the `WithdrawalRequest` that is created, or by subscribing to a webhook.
        """

        json = self._requester.execute_graphql(
            f"""
mutation RequestWithdrawal(
    $node_id: ID!
    $amount_sats: Long!
    $bitcoin_address: String!
    $withdrawal_mode: WithdrawalMode!
) {{
    request_withdrawal(input: {{
        node_id: $node_id
        amount_sats: $amount_sats
        bitcoin_address: $bitcoin_address
        withdrawal_mode: $withdrawal_mode
    }}) {{
        request {{
            ...WithdrawalRequestFragment
        }}
    }}
}}

{WithdrawalRequestFragment}
""",
            {
                "node_id": node_id,
                "amount_sats": amount_sats,
                "bitcoin_address": bitcoin_address,
                "withdrawal_mode": withdrawal_mode,
            },
            self.get_signing_key(node_id),
        )
        return WithdrawalRequest_from_json(
            self._requester, json["request_withdrawal"]["request"]
        )
