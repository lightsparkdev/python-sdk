# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Tuple
from unittest.mock import patch

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1, generate_private_key
from ecies import PrivateKey, decrypt
from uma.currency import Currency
from uma.kyc_status import KycStatus
from uma.payer_data import PayerDataOptions
from uma.public_key_cache import InMemoryPublicKeyCache, PubkeyResponse
from uma.uma import (
    create_compliance_payer_data,
    create_lnurlp_request_url,
    create_lnurlp_response,
    create_pay_req_response,
    create_pay_request,
    fetch_public_key_for_vasp,
    is_uma_lnurlp_query,
    parse_lnurlp_request,
    parse_lnurlp_response,
    parse_pay_req_response,
    parse_pay_request,
    verify_pay_request_signature,
    verify_uma_lnurlp_query_signature,
    verify_uma_lnurlp_response_signature,
)
from uma.uma_invoice_creator import IUmaInvoiceCreator


def test_fetch_public_key() -> None:
    cache = InMemoryPublicKeyCache()
    vasp_domain = "vasp2.com"
    timestamp = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
    expected_pubkey = PubkeyResponse(
        signing_pubkey=secrets.token_bytes(16),
        encryption_pubkey=secrets.token_bytes(16),
        expiration_timestamp=datetime.fromtimestamp(timestamp, timezone.utc),
    )
    url = "https://vasp2.com/.well-known/lnurlpubkey"

    with patch(
        "uma.uma._run_http_get",
        return_value=json.dumps(expected_pubkey.to_dict()),
    ) as mock:
        pubkey_response = fetch_public_key_for_vasp(vasp_domain, cache)
        mock.assert_called_once_with(url)
        assert pubkey_response == expected_pubkey
        assert cache.fetch_public_key_for_vasp(vasp_domain) == expected_pubkey


def _create_key_pair() -> Tuple[bytes, bytes]:
    private_key = generate_private_key(SECP256K1())
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return (private_key_bytes, public_key_bytes)


def test_pay_request_create_and_parse() -> None:
    (
        sender_signing_private_key_bytes,
        sender_signing_public_key_bytes,
    ) = _create_key_pair()

    (
        receiver_encryption_private_key_bytes,
        receiver_encryption_public_key_bytes,
    ) = _create_key_pair()

    travel_rule_info = "some TR info for VASP2"
    currency_code = "USD"
    amount = 100
    payer_identifier = "$alice@vasp1.com"
    payer_kyc_status = KycStatus.VERIFIED
    utxo_callback = "/api/lnurl/utxocallback?txid=1234"
    node_pubkey = "dummy_node_key"
    payer_compliance_data = create_compliance_payer_data(
        signing_private_key=sender_signing_private_key_bytes,
        receiver_encryption_pubkey=receiver_encryption_public_key_bytes,
        payer_identifier=payer_identifier,
        travel_rule_info=travel_rule_info,
        payer_kyc_status=payer_kyc_status,
        payer_utxos=["abcdef12345"],
        payer_node_pubkey=node_pubkey,
        utxo_callback=utxo_callback,
    )
    pay_request = create_pay_request(
        currency_code=currency_code,
        amount=amount,
        payer_identifier=payer_identifier,
        payer_name=None,
        payer_email=None,
        payer_compliance=payer_compliance_data,
    )

    json_payload = pay_request.to_json()
    result_pay_request = parse_pay_request(json_payload)
    assert pay_request == result_pay_request
    verify_pay_request_signature(pay_request, sender_signing_public_key_bytes)

    # test invalid signature
    pay_request.payer_data.compliance.signature = (  # pyre-ignore: [16]
        secrets.token_hex()
    )
    with pytest.raises(InvalidSignature):
        verify_pay_request_signature(pay_request, sender_signing_public_key_bytes)

    # verify encryption
    encrypted_travel_rule_info = (
        result_pay_request.payer_data.compliance.encrypted_travel_rule_info  # pyre-ignore: [16]
    )
    private_key = PrivateKey.from_der(receiver_encryption_private_key_bytes)
    assert (
        decrypt(private_key.secret, bytes.fromhex(encrypted_travel_rule_info)).decode()
        == travel_rule_info
    )


def test_lnurlp_query_missing_params() -> None:
    url = "https://vasp2.com/.well-known/lnurlp/bob?nonce=12345&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/.well-known/lnurlp/bob?signature=signature&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/.well-known/lnurlp/bob?signature=signature&nonce=12345&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    # isSubjectToTravelRule is optional
    url = "https://vasp2.com/.well-known/lnurlp/bob?signature=signature&nonce=12345&vaspDomain=vasp1.com&timestamp=12345678&umaVersion=0.1"
    assert is_uma_lnurlp_query(url)

    url = "https://vasp2.com/.well-known/lnurlp/bob?signature=signature&nonce=12345&vaspDomain=vasp1.com&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/.well-known/lnurlp/bob?signature=signature&nonce=12345&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/.well-known/lnurlp/bob"
    assert not is_uma_lnurlp_query(url)


def test_lnurlp_query_invalid_path() -> None:
    url = "https://vasp2.com/.well-known/lnurla/bob?signature=signature&nonce=12345&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/bob?signature=signature&nonce=12345&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)

    url = "https://vasp2.com/?signature=signature&nonce=12345&vaspDomain=vasp1.com&umaVersion=0.1&isSubjectToTravelRule=true&timestamp=12345678"
    assert not is_uma_lnurlp_query(url)


def test_lnurlp_request_url_create_and_parse() -> None:
    (
        sender_signing_private_key_bytes,
        sender_signing_public_key_bytes,
    ) = _create_key_pair()

    receiver_address = "bob@vasp2.com"
    sender_vasp_domain = "vasp1.com"
    is_subject_to_travel_rule = False

    url = create_lnurlp_request_url(
        signing_private_key=sender_signing_private_key_bytes,
        receiver_address=receiver_address,
        sender_vasp_domain=sender_vasp_domain,
        is_subject_to_travel_rule=is_subject_to_travel_rule,
    )

    request = parse_lnurlp_request(url)
    assert request.receiver_address == receiver_address
    assert request.is_subject_to_travel_rule == is_subject_to_travel_rule
    assert request.vasp_domain == sender_vasp_domain

    verify_uma_lnurlp_query_signature(request, sender_signing_public_key_bytes)

    # test invalid signature
    request.signature = secrets.token_hex()
    with pytest.raises(InvalidSignature):
        verify_uma_lnurlp_query_signature(request, sender_signing_public_key_bytes)


class DummyUmaInvoiceCreator(IUmaInvoiceCreator):
    DUMMY_INVOICE = "DUMMY_INVOICE"

    def create_uma_invoice(
        self,
        amount_msats: int,
        metadata: str,
    ) -> str:
        return self.DUMMY_INVOICE


def test_pay_req_response_create_and_parse() -> None:
    sender_signing_private_key_bytes, _ = _create_key_pair()
    _, receiver_encryption_public_key_bytes = _create_key_pair()

    travel_rule_info = "some TR info for VASP2"
    currency_code = "USD"
    amount = 100
    payer_identifier = "$alice@vasp1.com"
    payer_kyc_status = KycStatus.VERIFIED
    sender_utxo_callback = "/sender_api/lnurl/utxocallback?txid=1234"
    node_pubkey = "dummy_node_key"
    pay_request = create_pay_request(
        currency_code=currency_code,
        amount=amount,
        payer_identifier=payer_identifier,
        payer_name=None,
        payer_email=None,
        payer_compliance=create_compliance_payer_data(
            signing_private_key=sender_signing_private_key_bytes,
            receiver_encryption_pubkey=receiver_encryption_public_key_bytes,
            payer_identifier=payer_identifier,
            travel_rule_info=travel_rule_info,
            payer_kyc_status=payer_kyc_status,
            payer_utxos=["abcdef12345"],
            payer_node_pubkey=node_pubkey,
            utxo_callback=sender_utxo_callback,
        ),
    )

    msats_per_currency_unit = 34_150
    receiver_fees_msats = 2_000
    receiver_utxos = ["abcdef12345"]
    receiver_utxo_callback = "/receiver_api/lnurl/utxocallback?txid=1234"
    receiver_node_pubkey = "dummy_pub_key"
    invoice_creator = DummyUmaInvoiceCreator()
    response = create_pay_req_response(
        request=pay_request,
        invoice_creator=invoice_creator,
        metadata=_create_metadata(),
        currency_code=currency_code,
        msats_per_currency_unit=msats_per_currency_unit,
        receiver_fees_msats=receiver_fees_msats,
        receiver_utxos=receiver_utxos,
        receiver_node_pubkey=receiver_node_pubkey,
        utxo_callback=receiver_utxo_callback,
    )

    assert response == parse_pay_req_response(response.to_json())
    assert response.encoded_invoice == invoice_creator.DUMMY_INVOICE
    assert response.compliance.utxo_callback == receiver_utxo_callback
    assert response.compliance.utxos == receiver_utxos
    assert response.compliance.node_pubkey == receiver_node_pubkey
    assert response.payment_info.currency_code == currency_code
    assert response.payment_info.multiplier == msats_per_currency_unit
    assert response.payment_info.exchange_fees_msats == receiver_fees_msats


def _create_metadata() -> str:
    metadata = [
        ["text/plain", "Pay to vasp2.com user $bob"],
        ["text/identifier", "bob@vasp2.com"],
    ]
    return json.dumps(metadata)


def test_lnurlp_response_create_and_parse() -> None:
    sender_signing_private_key_bytes, _ = _create_key_pair()
    (
        receiver_signing_private_key_bytes,
        receiver_signing_public_key_bytes,
    ) = _create_key_pair()

    receiver_address = "bob@vasp2.com"
    lnurlp_request_url = create_lnurlp_request_url(
        signing_private_key=sender_signing_private_key_bytes,
        receiver_address=receiver_address,
        sender_vasp_domain="vasp1.com",
        is_subject_to_travel_rule=True,
    )
    lnurlp_request = parse_lnurlp_request(lnurlp_request_url)
    metadata = _create_metadata()
    callback = "https://vasp2.com/api/lnurl/payreq/$bob"
    min_sendable_sats = 1
    max_sendable_sats = 10_000_000
    payer_data_options = PayerDataOptions(
        name_required=False, email_required=False, compliance_required=True
    )
    currencies = [
        Currency(
            code="USD",
            name="US Dollar",
            symbol="$",
            millisatoshi_per_unit=34_150,
            max_sendable=max_sendable_sats,
            min_sendable=min_sendable_sats,
        )
    ]
    is_subject_to_travel_rule = True
    receiver_kyc_status = KycStatus.VERIFIED
    response = create_lnurlp_response(
        request=lnurlp_request,
        signing_private_key=receiver_signing_private_key_bytes,
        requires_travel_rule_info=is_subject_to_travel_rule,
        callback=callback,
        encoded_metadata=metadata,
        min_sendable_sats=min_sendable_sats,
        max_sendable_sats=max_sendable_sats,
        payer_data_options=payer_data_options,
        currency_options=currencies,
        receiver_kyc_status=receiver_kyc_status,
    )

    result_response = parse_lnurlp_response(response.to_json())
    assert response == result_response
    assert result_response.tag == "payRequest"
    assert result_response.callback == callback
    assert result_response.max_sendable == max_sendable_sats
    assert result_response.min_sendable == min_sendable_sats
    assert result_response.encoded_metadata == metadata
    assert result_response.currencies == currencies
    assert result_response.currencies == currencies
    assert result_response.required_payer_data == payer_data_options
    assert result_response.compliance.kyc_status == receiver_kyc_status
    assert (
        result_response.compliance.is_subject_to_travel_rule
        == is_subject_to_travel_rule
    )
    assert result_response.compliance.receiver_identifier == receiver_address

    verify_uma_lnurlp_response_signature(
        result_response, receiver_signing_public_key_bytes
    )

    # test invalid signature
    result_response.compliance.signature = secrets.token_hex()
    with pytest.raises(InvalidSignature):
        verify_uma_lnurlp_response_signature(
            result_response, receiver_signing_public_key_bytes
        )
