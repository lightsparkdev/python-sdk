import json
from base64 import b64encode
from abc import ABC, abstractmethod

from lightspark_crypto import (  # pyre-ignore[21]
    sign_ecdsa,
    LightsparkSigner,
    Network,
    Seed,
)

from lightspark.objects.BitcoinNetwork import BitcoinNetwork
from lightspark.utils.crypto import sign_payload
from lightspark.exceptions import LightsparkException


class SigningKey(ABC):
    key: bytes

    @abstractmethod
    def sign_payload(self, payload: bytes) -> str:
        pass


class RSASigningKey(SigningKey):
    def __init__(self, key: bytes) -> None:
        self.key = key

    def sign_payload(self, payload: bytes) -> str:
        return sign_payload(payload, self.key)


class Secp256k1SigningKey(SigningKey):
    def __init__(self, master_seed: bytes, bitcoin_network: BitcoinNetwork) -> None:
        seed = Seed(master_seed)
        if bitcoin_network == BitcoinNetwork.MAINNET:
            network = Network.BITCOIN
        elif bitcoin_network == BitcoinNetwork.TESTNET:
            network = Network.TESTNET
        elif bitcoin_network == BitcoinNetwork.REGTEST:
            network = Network.REGTEST
        else:
            raise LightsparkException("SIGNING_ERROR", "Invalid bitcoin network")
        signer = LightsparkSigner(seed, network)
        self.key = signer.derive_private_key("m/5")

    def sign_payload(self, payload: bytes) -> str:
        sig = sign_ecdsa(payload, self.key)
        return json.dumps(
            {
                "v": 1,
                "signature": b64encode(sig).decode("ascii"),
            }
        )
