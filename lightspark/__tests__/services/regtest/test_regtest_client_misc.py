import logging
import os

import lightspark
from lightspark.__tests__.test_utilities import none_throws

log = logging.getLogger("python_sdk_test_regtest_client_misc")

LIGHTSPARK_API_ENDPOINT = os.environ["LIGHTSPARK_API_ENDPOINT"]
LIGHTSPARK_API_TOKEN_CLIENT_ID = os.environ["LIGHTSPARK_API_TOKEN_CLIENT_ID"]
LIGHTSPARK_API_TOKEN_CLIENT_SECRET = os.environ["LIGHTSPARK_API_TOKEN_CLIENT_SECRET"]
LIGHTSPARK_RS_NODE_ID = os.environ["LIGHTSPARK_RS_NODE_ID"]
LIGHTSPARK_RS_NODE_ID_2 = os.environ["LIGHTSPARK_RS_NODE_ID_2"]
LIGHTSPARK_API_TOKEN_CLIENT_ID_2 = os.environ["LIGHTSPARK_API_TOKEN_CLIENT_ID_2"]
LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2 = os.environ[
    "LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2"
]
LIGHTSPARK_RS_MASTER_SEED = os.environ["LIGHTSPARK_RS_MASTER_SEED"]
LIGHTSPARK_RS_MASTER_SEED_2 = os.environ["LIGHTSPARK_RS_MASTER_SEED_2"]


def test_create_invoice() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    invoice = client.create_invoice(LIGHTSPARK_RS_NODE_ID, 10_000_000)
    log.info(invoice)
    log.info("===test_create_invoice===SUCCEEDED\n")


def test_get_channel_utxos() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    node = none_throws(
        client.get_entity(LIGHTSPARK_RS_NODE_ID, lightspark.LightsparkNode)
    )
    utxos = node.uma_prescreening_utxos
    log.info(utxos)
    log.info("===test_get_channel_utxos===SUCCEEDED\n")


def test_get_funding_address() -> None:
    client2 = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID_2,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    seed_bytes2 = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED_2)
    client2.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID_2,
        seed_bytes2,
        lightspark.BitcoinNetwork.REGTEST,
    )
    node2 = none_throws(
        client2.get_entity(LIGHTSPARK_RS_NODE_ID_2, lightspark.LightsparkNode)
    )
    CREATE_NODE_WALLET_ADDRESS_MUTATION = f"""
    mutation CreateNodeWalletAddress {{
        create_node_wallet_address(input: {{
            node_id: "{node2.id}"
        }}) {{
            wallet_address
        }}
    }}
    """
    response = client2.execute_graphql_request(CREATE_NODE_WALLET_ADDRESS_MUTATION)
    walletAddress = response["create_node_wallet_address"]["wallet_address"]
    log.info("Wallet address: %s", walletAddress)
    log.info("===test_get_funding_address===SUCCEEDED\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    test_create_invoice()
    test_get_channel_utxos()
    test_get_funding_address()
