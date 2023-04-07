# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
from base64 import b64decode, b64encode
from hashlib import pbkdf2_hmac
from secrets import token_bytes
from typing import Tuple

from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from lightspark.exceptions import LightsparkException

IV_LEN = 12
KEY_LEN = 32
SALT_LEN = 16
ITERATIONS = 500000


def derive_key(password: bytes, salt: bytes, iterations: int) -> bytes:
    derived = pbkdf2_hmac("sha256", password, salt, iterations, KEY_LEN)
    return derived


def derive_key_iv(
    password: bytes, salt: bytes, iterations: int, length: int
) -> Tuple[bytes, bytes]:
    derived = pbkdf2_hmac("sha256", password, salt, iterations, length)
    return derived[:KEY_LEN], derived[KEY_LEN:]


def encrypt(plaintext: bytes, password: str) -> Tuple[str, str]:
    salt = token_bytes(SALT_LEN)
    key, iv = derive_key_iv(password.encode("utf8"), salt, ITERATIONS, KEY_LEN + IV_LEN)
    encryptor = AESGCM(key)
    ciphertext = encryptor.encrypt(iv, plaintext, None)
    header = {"v": 4, "i": ITERATIONS}
    return json.dumps(header), b64encode(salt + ciphertext).decode()


def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(plaintext) + unpadder.finalize()


def decrypt_gcm(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    decryptor = AESGCM(key)
    return decryptor.decrypt(iv, ciphertext, None)


def decrypt_private_key(
    cipher_version: str, encrypted_value: str, password: str
) -> bytes:
    decoded = b64decode(encrypted_value)

    if cipher_version == "AES_256_CBC_PBKDF2_5000_SHA256":
        header = {"v": 0, "i": 5000}
        decoded = decoded[8:]
    else:
        header = json.loads(cipher_version)
    if header.get("lsv", 0) == 2:
        header["v"] = 3

    if header["v"] < 0 or header["v"] > 4:
        raise LightsparkException("CRYPTO_EXCEPTION", f"Unknown version {header['v']}")

    if header["v"] == 3:
        salt = decoded[-8:]
        nonce = decoded[0:12]
        ciphertext = decoded[12:-8]
        key = derive_key(password.encode("utf8"), salt, header["i"])
        plaintext = decrypt_gcm(ciphertext, key, nonce)
        return plaintext

    salt_len = 8 if header["v"] < 4 else 16
    iv_len = 16 if header["v"] < 4 else 12

    salt = decoded[:salt_len]
    ciphertext = decoded[salt_len:]

    key, iv = derive_key_iv(
        password.encode("utf8"), salt, header["i"], KEY_LEN + iv_len
    )
    plaintext = (
        decrypt_cbc(ciphertext, key, iv)
        if header["v"] < 2
        else decrypt_gcm(ciphertext, key, iv)
    )

    return plaintext


def sign_payload(payload: bytes, signing_key: bytes) -> str:
    if signing_key[0] != 48:
        signing_key = b64decode(signing_key)
    key = serialization.load_der_private_key(signing_key, password=None)

    signature = key.sign(
        payload,
        asymmetric_padding.PSS(
            mgf=asymmetric_padding.MGF1(hashes.SHA256()),
            salt_length=asymmetric_padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return json.dumps(
        {
            "v": 1,
            "signature": b64encode(signature).decode("ascii"),
        }
    )
