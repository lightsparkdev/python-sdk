# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any, Dict, List, Mapping, Optional, Tuple, Type, TypeVar

import jwt
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)
from lightspark.exceptions import LightsparkException
from lightspark.objects.Account import Account
from lightspark.objects.Account import from_json as Account_from_json
from lightspark.objects.all_entities import get_entity
from lightspark.objects.ApiToken import ApiToken
from lightspark.objects.ApiToken import from_json as ApiToken_from_json
from lightspark.objects.BitcoinNetwork import BitcoinNetwork
from lightspark.objects.ComplianceProvider import ComplianceProvider
from lightspark.objects.CurrencyAmount import CurrencyAmount
from lightspark.objects.CurrencyAmount import from_json as CurrencyAmount_from_json
from lightspark.objects.Entity import Entity
from lightspark.objects.FeeEstimate import FeeEstimate
from lightspark.objects.FeeEstimate import from_json as FeeEstimate_from_json
from lightspark.objects.IncomingPayment import IncomingPayment
from lightspark.objects.IncomingPayment import from_json as IncomingPayment_from_json
from lightspark.objects.IncomingPaymentsForInvoiceQueryOutput import (
    from_json as IncomingPaymentsForInvoiceQueryOutput_from_json,
)
from lightspark.objects.Invoice import Invoice
from lightspark.objects.Invoice import from_json as Invoice_from_json
from lightspark.objects.InvoiceData import InvoiceData
from lightspark.objects.InvoiceData import from_json as InvoiceData_from_json
from lightspark.objects.InvoiceType import InvoiceType
from lightspark.objects.LightningFeeEstimateOutput import (
    from_json as LightningFeeEstimateOutput_from_json,
)
from lightspark.objects.LightningTransaction import LightningTransaction
from lightspark.objects.LightningTransaction import (
    from_json as LightningTransaction_from_json,
)
from lightspark.objects.OutgoingPayment import OutgoingPayment
from lightspark.objects.OutgoingPayment import from_json as OutgoingPayment_from_json
from lightspark.objects.PaymentDirection import PaymentDirection
from lightspark.objects.Permission import Permission
from lightspark.objects.RegionCode import RegionCode
from lightspark.objects.RiskRating import RiskRating
from lightspark.objects.TransactionStatus import TransactionStatus
from lightspark.objects.UmaInvitation import UmaInvitation
from lightspark.objects.UmaInvitation import from_json as UmaInvitation_from_json
from lightspark.objects.WithdrawalMode import WithdrawalMode
from lightspark.objects.WithdrawalRequest import WithdrawalRequest
from lightspark.objects.WithdrawalRequest import (
    from_json as WithdrawalRequest_from_json,
)
from lightspark.requests.requester import Requester
from lightspark.scripts.bitcoin_fee_estimate import BITCOIN_FEE_ESTIMATE_QUERY
from lightspark.scripts.cancel_invoice import CANCEL_INVOICE_MUTATION
from lightspark.scripts.claim_uma_invitation import (
    CLAIM_UMA_INVITATION_MUTATION,
    CLAIM_UMA_INVITATION_WITH_INCENTIVES_MUTATION,
)
from lightspark.scripts.create_api_token import CREATE_API_TOKEN_MUTATION
from lightspark.scripts.create_invoice import CREATE_INVOICE_MUTATION
from lightspark.scripts.create_lnurl_invoice import CREATE_LNURL_INVOICE_MUTATION
from lightspark.scripts.create_node_address import CREATE_NODE_ADDRESS_MUTATION
from lightspark.scripts.create_test_mode_invoice import (
    CREATE_TEST_MODE_INVOICE_MUTATION,
)
from lightspark.scripts.create_test_mode_payment import (
    CREATE_TEST_MODE_PAYMENT_MUTATION,
)
from lightspark.scripts.create_uma_invitation import (
    CREATE_UMA_INVITATION_MUTATION,
    CREATE_UMA_INVITATION_WITH_INCENTIVES_MUTATION,
)
from lightspark.scripts.create_uma_invoice import CREATE_UMA_INVOICE_MUTATION
from lightspark.scripts.current_account import CURRENT_ACCOUNT_QUERY
from lightspark.scripts.decoded_payment_request import DECODED_PAYMENT_REQUEST_QUERY
from lightspark.scripts.delete_api_token import DELETE_API_TOKEN_MUTATION
from lightspark.scripts.fail_htlcs import FAIL_HTLCS_MUTATION
from lightspark.scripts.fetch_uma_invitation import FETCH_UMA_INVITATION_QUERY
from lightspark.scripts.fund_node import FUND_NODE_MUTATION
from lightspark.scripts.incoming_payments_for_invoice import (
    INCOMING_PAYMENTS_FOR_INVOICE_QUERY,
)
from lightspark.scripts.invoice_for_payment_hash import INVOICE_FOR_PAYMENT_HASH_QUERY
from lightspark.scripts.lightning_fee_estimate_for_invoice import (
    LIGHTNING_FEE_ESTIMATE_FOR_INVOICE_QUERY,
)
from lightspark.scripts.lightning_fee_estimate_for_node import (
    LIGHTNING_FEE_ESTIMATE_FOR_NODE_QUERY,
)
from lightspark.scripts.outgoing_payment_for_idempotency_key import (
    OUTGOING_PAYMENT_FOR_IDEMPOTENCY_KEY_QUERY,
)
from lightspark.scripts.outgoing_payments_for_invoice import (
    OUTGOING_PAYMENTS_FOR_INVOICE_QUERY,
)
from lightspark.scripts.outgoing_payments_for_payment_hash import (
    OUTGOING_PAYMENTS_FOR_PAYMENT_HASH_QUERY,
)
from lightspark.scripts.pay_invoice import PAY_INVOICE_MUTATION
from lightspark.scripts.pay_uma_invoice import PAY_UMA_INVOICE_MUTATION
from lightspark.scripts.recover_node_signing_key import RECOVER_NODE_SIGNING_KEY_QUERY
from lightspark.scripts.register_payment import REGISTER_PAYMENT_MUTATION
from lightspark.scripts.request_withdrawal import REQUEST_WITHDRAWAL_MUTATION
from lightspark.scripts.screen_node import SCREEN_NODE_MUTATION
from lightspark.scripts.send_payment import SEND_PAYMENT_MUTATION
from lightspark.utils.crypto import decrypt_private_key
from lightspark.utils.enums import parse_enum
from lightspark.utils.signing_key import RSASigningKey, Secp256k1SigningKey, SigningKey

logger = logging.getLogger("lightspark")

ENTITY = TypeVar("ENTITY", bound=Entity)


@dataclass
class LightsparkSyncClient:
    _requester: Requester
    _node_private_keys: Dict[str, SigningKey]

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
            CREATE_API_TOKEN_MUTATION,
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
        expiry_secs: Optional[int] = None,
    ) -> Invoice:
        logger.info("Creating an invoice for node %s.", node_id)
        variables = {
            "amount_msats": amount_msats,
            "node_id": node_id,
            "memo": memo,
            "invoice_type": invoice_type,
        }
        if expiry_secs is not None:
            variables["expiry_secs"] = expiry_secs
        json = self._requester.execute_graphql(CREATE_INVOICE_MUTATION, variables)

        return Invoice_from_json(self._requester, json["create_invoice"]["invoice"])

    def create_lnurl_invoice(
        self,
        node_id: str,
        amount_msats: int,
        metadata: str,
        expiry_secs: Optional[int] = None,
    ) -> Invoice:
        """Generates a Lightning Invoice (follows the Bolt 11 specification) to request a payment
        from another Lightning Node. This should only be used for generating invoices for LNURLs,
        with `create_invoice` preferred in the general case.

        Args:
            node_id (str): The ID of the node from which to create the invoice.
            amount_sats (int): The amount for which the invoice should be created, in millisatoshis.
            will be added.
            metadata (str): The LNURL metadata payload field in the initial payreq response. This
            will be hashed and present in the h-tag (SHA256 purpose of payment) of the resulting
            Bolt 11 invoice.
            expiry_secs (int, optional): The number of seconds after which the invoice will expire.
            Defaults to 1 day.

        Returns:
            Invoice: An `Invoice` object representing the generated invoice.
        """
        logger.info("Creating an lnurl invoice for node %s.", node_id)
        variables = {
            "amount_msats": amount_msats,
            "node_id": node_id,
            "metadata_hash": sha256(metadata.encode("utf-8")).hexdigest(),
        }
        if expiry_secs is not None:
            variables["expiry_secs"] = expiry_secs
        json = self._requester.execute_graphql(CREATE_LNURL_INVOICE_MUTATION, variables)

        return Invoice_from_json(
            self._requester, json["create_lnurl_invoice"]["invoice"]
        )

    def cancel_invoice(
        self,
        invoice_id: str,
    ) -> Invoice:
        """Cancels an existing unpaid invoice and returns that invoice. Cancelled invoices cannot be paid.

        Args:
            invoice_id (str): The ID of the invoice to cancel.

        Returns:
            Invoice: An `Invoice` object representing the cancelled invoice.
        """
        logger.info("Canceling an invoice with id %s.", invoice_id)
        json = self._requester.execute_graphql(
            CANCEL_INVOICE_MUTATION,
            {"invoice_id": invoice_id},
        )

        return Invoice_from_json(self._requester, json["cancel_invoice"]["invoice"])

    def create_node_wallet_address(
        self,
        node_id: str,
    ) -> str:
        logger.info("Creating a wallet address for node %s.", node_id)
        json = self._requester.execute_graphql(
            CREATE_NODE_ADDRESS_MUTATION,
            {"node_id": node_id},
        )
        return json["create_node_wallet_address"]["wallet_address"]

    def create_test_mode_invoice(
        self,
        local_node_id: str,
        amount_msats: int,
        memo: Optional[str] = None,
        invoice_type: Optional[InvoiceType] = None,
    ) -> str:
        logger.info("Creating a test invoice for node %s.", local_node_id)
        json = self._requester.execute_graphql(
            CREATE_TEST_MODE_INVOICE_MUTATION,
            {
                "amount_msats": amount_msats,
                "local_node_id": local_node_id,
                "memo": memo,
                "invoice_type": invoice_type,
            },
        )

        return json["create_test_mode_invoice"]["encoded_payment_request"]

    def create_test_mode_payment(
        self,
        local_node_id: str,
        encoded_invoice: str,
        amount_msats: Optional[int] = None,
    ) -> IncomingPayment:
        variables: Dict[str, Any] = {
            "local_node_id": local_node_id,
            "encoded_invoice": encoded_invoice,
        }
        if amount_msats is not None:
            variables["amount_msats"] = amount_msats

        json = self._requester.execute_graphql(
            CREATE_TEST_MODE_PAYMENT_MUTATION,
            variables,
        )
        return IncomingPayment_from_json(
            self._requester, json["create_test_mode_payment"]["incoming_payment"]
        )

    def create_uma_invoice(
        self,
        node_id: str,
        amount_msats: int,
        metadata: str,
        expiry_secs: Optional[int] = None,
        signing_private_key: Optional[bytes] = None,
        receiver_identifier: Optional[str] = None,
    ) -> Invoice:
        """Creates a new invoice for the UMA protocol. The metadata is hashed and included in the invoice. This API
        generates a Lightning Invoice (follows the Bolt 11 specification) to request a payment from another Lightning Node.
        This should only be used for generating invoices for UMA, with `create_invoice` preferred in the general case.

        Args:
            node_id: The node ID for which to create an invoice.
            amount_msats: The amount of the invoice in msats. You can create a zero-amount invoice to accept any payment amount.
            metadata: The LNURL metadata payload field in the initial payreq response. This wil be hashed and present in the
            h-tag (SHA256 purpose of payment) of the resulting Bolt 11 invoice. See
            [this spec](https://github.com/lnurl/luds/blob/luds/06.md#pay-to-static-qrnfclink) for details.
            expiry_secs: The number of seconds until the invoice expires. Defaults to 600.
            signing_private_key: The receiver's signing private key. Used to hash the receiver identifier.
            receiver_identifier: Optional identifier of the receiver. If provided, this will be hashed using a monthly-rotated
            seed and used for anonymized analysis.
        """
        receiver_hash = None
        if receiver_identifier is not None:
            if signing_private_key is None:
                raise LightsparkException(
                    "CreateUmaInvoiceError",
                    "Receiver identifier provided without signing private key",
                )
            receiver_hash = self.hash_uma_identifier(
                receiver_identifier, signing_private_key
            )

        variables = {
            "amount_msats": amount_msats,
            "node_id": node_id,
            "metadata_hash": sha256(metadata.encode("utf-8")).hexdigest(),
            "expiry_secs": expiry_secs if expiry_secs is not None else 600,
        }
        if receiver_hash is not None:
            variables["receiver_hash"] = receiver_hash
        logger.info("Creating an uma invoice for node %s.", node_id)
        json = self._requester.execute_graphql(
            CREATE_UMA_INVOICE_MUTATION,
            variables,
        )

        return Invoice_from_json(self._requester, json["create_uma_invoice"]["invoice"])

    def delete_api_token(self, api_token_id: str) -> None:
        logger.info("Deleting API token %s.", api_token_id)
        self._requester.execute_graphql(
            DELETE_API_TOKEN_MUTATION,
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

    def generate_jwt_key(self) -> Tuple[str, str]:
        key = Ed448PrivateKey.generate()
        return (
            key.public_key()
            .public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
            .decode(),
            key.private_bytes(
                Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
            ).decode(),
        )

    def generate_wallet_jwt(
        self,
        private_key_pem: str,
        third_party_id: str,
        test_mode: bool = False,
        duration: timedelta = timedelta(minutes=1),
        algorithm: str = "EdDSA",
    ) -> str:
        payload = {
            "aud": "https://api.lightspark.com",
            "exp": datetime.now(timezone.utc) + duration,
            "iat": datetime.now(timezone.utc),
            "sub": third_party_id,
            "test": test_mode,
        }
        return jwt.encode(payload, private_key_pem, algorithm)

    def get_current_account(
        self,
    ) -> Account:
        logger.info("Fetching current account.")
        json = self._requester.execute_graphql(
            CURRENT_ACCOUNT_QUERY,
            {},
        )
        return Account_from_json(self._requester, json["current_account"])

    def get_decoded_payment_request(self, encoded_payment_request: str) -> InvoiceData:
        logger.info(
            "Decoding payment request starting with %s...",
            encoded_payment_request[0:10],
        )
        json = self._requester.execute_graphql(
            DECODED_PAYMENT_REQUEST_QUERY,
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
            BITCOIN_FEE_ESTIMATE_QUERY,
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
            LIGHTNING_FEE_ESTIMATE_FOR_INVOICE_QUERY,
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
            LIGHTNING_FEE_ESTIMATE_FOR_NODE_QUERY,
            {
                "node_id": node_id,
                "destination_node_public_key": destination_node_public_key,
                "amount_msats": amount_msats,
            },
        )
        return LightningFeeEstimateOutput_from_json(
            self._requester, json["lightning_fee_estimate_for_node"]
        ).fee_estimate

    def load_node_signing_key(self, node_id: str, signing_key: SigningKey) -> None:
        logger.info("Loading the signing key for node %s", node_id)
        self._node_private_keys[node_id] = signing_key

    def recover_node_signing_key(self, node_id: str, node_password: str) -> SigningKey:
        logger.info("Recovering the signing key for node %s", node_id)
        json = self._requester.execute_graphql(
            RECOVER_NODE_SIGNING_KEY_QUERY,
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

        signing_key = RSASigningKey(decrypted_private_key)

        self.load_node_signing_key(node_id=node_id, signing_key=signing_key)
        return signing_key

    def provide_node_master_seed(
        self, node_id: str, master_seed: bytes, bitcoin_network: BitcoinNetwork
    ) -> None:
        signing_key = Secp256k1SigningKey(master_seed, bitcoin_network)
        self.load_node_signing_key(node_id=node_id, signing_key=signing_key)

    def pay_invoice(
        self,
        node_id: str,
        encoded_invoice: str,
        timeout_secs: int,
        maximum_fees_msats: int,
        amount_msats: Optional[int] = None,
        idempotency_key: Optional[str] = None,
    ) -> OutgoingPayment:
        variables = {
            "node_id": node_id,
            "encoded_invoice": encoded_invoice,
            "timeout_secs": timeout_secs,
            "maximum_fees_msats": maximum_fees_msats,
        }
        if amount_msats is not None:
            variables["amount_msats"] = amount_msats
        if idempotency_key is not None:
            variables["idempotency_key"] = idempotency_key
        json = self._requester.execute_graphql(
            PAY_INVOICE_MUTATION,
            variables,
            self.get_signing_key(node_id),
        )
        return OutgoingPayment_from_json(
            self._requester, json["pay_invoice"]["payment"]
        )

    def pay_uma_invoice(
        self,
        node_id: str,
        encoded_invoice: str,
        timeout_secs: int,
        maximum_fees_msats: int,
        amount_msats: Optional[int] = None,
        idempotency_key: Optional[str] = None,
        signing_private_key: Optional[bytes] = None,
        sender_identifier: Optional[str] = None,
    ) -> OutgoingPayment:
        """Sends an UMA payment to a node on the Lightning Network, based on the invoice (as defined by the BOLT11
        specification) that you provide. This should only be used for paying UMA invoices, with `pay_invoice` preferred
        in the general case.

        Args:
            node_id: The ID of the node that will pay the invoice.
            encoded_invoice: The encoded invoice to pay.
            timeout_secs: A timeout for the payment in seconds.
            maximum_fees_msats: Maximum fees (in msats) to pay for the payment.
            amount_msats: The amount to pay in msats for a zero-amount invoice. Defaults to the full amount of the
            invoice. Note, this parameter can only be passed for a zero-amount invoice. Otherwise, the call will fail.
            idempotency_key: An optional key to ensure idempotency of the payment.
            signing_private_key: The sender's signing private key. Used to hash the sender identifier.
            sender_identifier: Optional identifier of the sender. If provided, this will be hashed using a monthly-rotated
            seed and used for anonymized analysis.
        """
        sender_hash = None
        if sender_identifier is not None:
            if signing_private_key is None:
                raise LightsparkException(
                    "PayUmaInvoiceError",
                    "Sender identifier provided without signing private key",
                )
            sender_hash = self.hash_uma_identifier(
                sender_identifier, signing_private_key
            )

        variables = {
            "node_id": node_id,
            "encoded_invoice": encoded_invoice,
            "timeout_secs": timeout_secs,
            "maximum_fees_msats": maximum_fees_msats,
        }
        if amount_msats is not None:
            variables["amount_msats"] = amount_msats
        if idempotency_key is not None:
            variables["idempotency_key"] = idempotency_key
        if sender_hash is not None:
            variables["sender_hash"] = sender_hash
        json = self._requester.execute_graphql(
            PAY_UMA_INVOICE_MUTATION,
            variables,
            self.get_signing_key(node_id),
        )
        return OutgoingPayment_from_json(
            self._requester, json["pay_uma_invoice"]["payment"]
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
            SEND_PAYMENT_MUTATION,
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

    def screen_node(self, provider: ComplianceProvider, node_pubkey: str) -> RiskRating:
        """
        Screens a lightning node using its public key. In order to call this API,
        you need to have the API key stored in your account setting page for the selected compliance provider.
        """
        json = self._requester.execute_graphql(
            SCREEN_NODE_MUTATION,
            {"provider": provider, "node_pubkey": node_pubkey},
        )
        return parse_enum(RiskRating, json["screen_node"]["rating"])

    def get_signing_key(self, node_id: str) -> SigningKey:
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
            FUND_NODE_MUTATION,
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
        idempotency_key: Optional[str] = None,
    ) -> WithdrawalRequest:
        """Withdraws funds from the account and sends it to the requested bitcoin address.

        Depending on the chosen mode, it will first take the funds from the wallet, and if applicable, close channels appropriately to recover enough funds and reopen channels with the remaining funds.
        The process is asynchronous and may take up to a few minutes. You can check the progress by polling the `WithdrawalRequest` that is created, or by subscribing to a webhook.
        """
        variables = {
            "node_id": node_id,
            "amount_sats": amount_sats,
            "bitcoin_address": bitcoin_address,
            "withdrawal_mode": withdrawal_mode,
        }
        if idempotency_key is not None:
            variables["idempotency_key"] = idempotency_key
        json = self._requester.execute_graphql(
            REQUEST_WITHDRAWAL_MUTATION,
            variables,
            self.get_signing_key(node_id),
        )
        return WithdrawalRequest_from_json(
            self._requester, json["request_withdrawal"]["request"]
        )

    def register_payment(
        self,
        provider: ComplianceProvider,
        payment_id: str,
        node_pubkey: str,
        direction: PaymentDirection,
    ) -> LightningTransaction:
        """
        Register a successful lightning payment with a selected compliance provider.
        In order to call this API, you need to have the API key stored in your account
        setting page for the selected compliance provider.

        Args:
            provider: The external compliance provider you have account with. You need to store the API key in your account seeting.
            payment_id: The ID of a lightning payment, which can be either an OutgoingPayment or an IncomingPayment.
            node_pubkey: The public key of the counterparty lightning node, which is the recipient node for an OutgoingPayment or the sender node for an IncomingPayment.
            direction: Indicates whether this payment is an OutgoingPayment or an IncomingPayment
        """
        json = self._requester.execute_graphql(
            REGISTER_PAYMENT_MUTATION,
            {
                "provider": provider,
                "node_pubkey": node_pubkey,
                "payment_id": payment_id,
                "direction": direction,
            },
        )
        return LightningTransaction_from_json(
            self._requester, json["register_payment"]["payment"]
        )

    def outgoing_payments_for_invoice(
        self,
        encoded_invoice: str,
        transaction_statuses: Optional[List[TransactionStatus]] = None,
    ) -> List[OutgoingPayment]:
        """
        Fetches the outgoing payments (if any) which have been made for a given invoice.

        Args:
            encoded_invoice: The encoded invoice for which to fetch the outgoing payments.
            transaction_statuses: The statuses of the transactions to fetch. If not specified, all transactions will be fetched.
        """

        variables: Dict[str, Any] = {"encoded_invoice": encoded_invoice}
        if transaction_statuses is not None:
            variables["transaction_statuses"] = transaction_statuses
        json = self._requester.execute_graphql(
            OUTGOING_PAYMENTS_FOR_INVOICE_QUERY, variables
        )
        if "outgoing_payments_for_invoice" not in json:
            return []
        if "payments" not in json["outgoing_payments_for_invoice"]:
            return []
        return [
            OutgoingPayment_from_json(self._requester, payment)
            for payment in json["outgoing_payments_for_invoice"]["payments"]
        ]

    def outgoing_payments_for_payment_hash(
        self,
        payment_hash: str,
        transaction_statuses: Optional[List[TransactionStatus]] = None,
    ) -> List[OutgoingPayment]:
        """
        Fetches the outgoing payments (if any) which have been made for a given payment hash.

        Args:
            payment_hash: The payment hash for which to fetch the outgoing payments.
            transaction_statuses: The statuses of the transactions to fetch. If not specified, all transactions will be fetched.
        """

        variables: Dict[str, Any] = {"payment_hash": payment_hash}
        if transaction_statuses is not None:
            variables["transaction_statuses"] = transaction_statuses
        json = self._requester.execute_graphql(
            OUTGOING_PAYMENTS_FOR_PAYMENT_HASH_QUERY, variables
        )
        if "outgoing_payments_for_payment_hash" not in json:
            return []
        if "payments" not in json["outgoing_payments_for_payment_hash"]:
            return []
        return [
            OutgoingPayment_from_json(self._requester, payment)
            for payment in json["outgoing_payments_for_payment_hash"]["payments"]
        ]

    def outgoing_payment_for_idempotency_key(
        self,
        idempotency_key: str,
    ) -> Optional[OutgoingPayment]:
        """
        Fetches the outgoing payment (if any) which have been made for a given idempotency key.
        """

        json = self._requester.execute_graphql(
            OUTGOING_PAYMENT_FOR_IDEMPOTENCY_KEY_QUERY,
            {"idempotency_key": idempotency_key},
        )
        if "outgoing_payment_for_idempotency_key" not in json:
            return None
        if "payment" not in json["outgoing_payment_for_idempotency_key"]:
            return None
        return OutgoingPayment_from_json(
            self._requester, json["outgoing_payment_for_idempotency_key"]["payment"]
        )

    def incoming_payments_for_invoice(
        self,
        invoice_id: str,
        transaction_statuses: Optional[List[TransactionStatus]] = None,
    ) -> List[IncomingPayment]:
        """
        Fetches the incoming payments (if any) which have been made for a given invoice.

        Args:
            invoice_id: The encoded invoice for which to fetch the incoming payments.
            transaction_statuses: The statuses of the transactions to fetch. If not specified, all transactions will be fetched.
        """

        variables: Dict[str, Any] = {"invoice_id": invoice_id}
        if transaction_statuses is not None:
            variables["transaction_statuses"] = transaction_statuses
        json = self._requester.execute_graphql(
            INCOMING_PAYMENTS_FOR_INVOICE_QUERY, variables
        )
        if "incoming_payments_for_invoice" not in json:
            return []
        output = IncomingPaymentsForInvoiceQueryOutput_from_json(
            self._requester, json["incoming_payments_for_invoice"]
        )
        return output.payments

    def invoice_for_payment_hash(
        self,
        payment_hash: str,
    ) -> Optional[Invoice]:
        """
        Fetches the invoice (if any) which have been created with a given payment hash.
        """

        json = self._requester.execute_graphql(
            INVOICE_FOR_PAYMENT_HASH_QUERY,
            {"payment_hash": payment_hash},
        )
        if "invoice_for_payment_hash" not in json:
            return None
        if "invoice" not in json["invoice_for_payment_hash"]:
            return None
        return Invoice_from_json(
            self._requester, json["invoice_for_payment_hash"]["invoice"]
        )

    def create_uma_invitation(
        self,
        inviter_uma: str,
    ) -> UmaInvitation:
        """
        Creates a new UMA invitation. If you are part of the incentive program, you should use the
        `create_uma_invitation_with_incentives` method instead.

        Args:
            inviter_uma: The UMA of the inviter.
        """
        json = self._requester.execute_graphql(
            CREATE_UMA_INVITATION_MUTATION,
            {
                "inviter_uma": inviter_uma,
            },
        )
        return UmaInvitation_from_json(
            self._requester, json["create_uma_invitation"]["invitation"]
        )

    def create_uma_invitation_with_incentives(
        self,
        inviter_uma: str,
        inviter_phone_number_e164: str,
        inviter_region: RegionCode,
    ) -> UmaInvitation:
        """
        Creates a new UMA invitation with incentives. If you are not part of the incentive program, you should use the
        `create_uma_invitation` method instead.

        Args:
            inviter_uma: The UMA of the inviter.
            inviter_phone_number_e164: The E.164 formatted phone number of the inviter.
            inviter_region: The region of the inviter.
        """
        json = self._requester.execute_graphql(
            CREATE_UMA_INVITATION_WITH_INCENTIVES_MUTATION,
            {
                "inviter_uma": inviter_uma,
                "inviter_phone_hash": self._hash_phone_number(
                    inviter_phone_number_e164
                ),
                "inviter_region": inviter_region.name,
            },
        )
        return UmaInvitation_from_json(
            self._requester, json["create_uma_invitation_with_incentives"]["invitation"]
        )

    def claim_uma_invitation(
        self,
        invitation_code: str,
        invitee_uma: str,
    ) -> None:
        """
        Claims a UMA invitation. If you are part of the incentive program, you should use the
        `claim_uma_invitation_with_incentives` method instead.

        Args:
            invitation_code: The invitation code of the invitation to claim.
            invitee_uma: The new UMA of the invitee.
        """
        self._requester.execute_graphql(
            CLAIM_UMA_INVITATION_MUTATION,
            {
                "invitation_code": invitation_code,
                "invitee_uma": invitee_uma,
            },
        )

    def claim_uma_invitation_with_incentives(
        self,
        invitation_code: str,
        invitee_uma: str,
        invitee_phone_number_e164: str,
        invitee_region: RegionCode,
    ) -> None:
        """
        Claims a UMA invitation with incentives. If you are not part of the incentive program, you should use the
        `claim_uma_invitation` method instead.

        Args:
            invitation_code: The invitation code of the invitation to claim.
            invitee_uma: The new UMA of the invitee.
            invitee_phone_number_e164: The E.164 formatted phone number of the invitee.
            invitee_region: The region of the invitee.
        """
        self._requester.execute_graphql(
            CLAIM_UMA_INVITATION_WITH_INCENTIVES_MUTATION,
            {
                "invitation_code": invitation_code,
                "invitee_uma": invitee_uma,
                "invitee_phone_hash": self._hash_phone_number(
                    invitee_phone_number_e164
                ),
                "invitee_region": invitee_region,
            },
        )

    def fetch_uma_invitation(
        self,
        invitation_code: str,
    ) -> Optional[UmaInvitation]:
        """
        Fetches a UMA invitation by its invitation code.

        Args:
            invitation_code: The invitation code of the invitation to fetch.
        """
        json = self._requester.execute_graphql(
            FETCH_UMA_INVITATION_QUERY,
            {
                "invitation_code": invitation_code,
            },
        )

        return (
            UmaInvitation_from_json(self._requester, json["uma_invitation_by_code"])
            if json["uma_invitation_by_code"]
            else None
        )

    def _hash_phone_number(self, phone_number_e164_format: str) -> str:
        match = E614_REGEX.search(phone_number_e164_format)
        if not match:
            raise LightsparkException(
                "InvalidPhoneNumber", "The phone number must follow the E.164 format."
            )
        return sha256(phone_number_e164_format.encode()).hexdigest()

    def hash_uma_identifier(self, identifier: str, signing_private_key: bytes) -> str:
        now = datetime.now(timezone.utc)
        input_data = identifier + f"{now.month}-{now.year}" + signing_private_key.hex()
        return sha256(input_data.encode()).hexdigest()

    def fail_htlcs(self, invoice_id: str, cancel_invoice: bool = True) -> str:
        """
        Fails all pending HTLCs associated with an invoice.

        Args:
            invoice_id: The ID of the invoice to fail.
            cancel_invoice: Whether to cancel the invoice after failing the HTLCs.
        """
        json = self._requester.execute_graphql(
            FAIL_HTLCS_MUTATION,
            {"invoice_id": invoice_id, "cancel_invoice": cancel_invoice},
        )

        return json["fail_htlcs"]["invoice"]["id"]


# pylint: disable=anomalous-backslash-in-string
E614_REGEX = re.compile("^\+?[1-9]\d{1,14}$")
