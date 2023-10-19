import logging
import os

import lightspark
from lightspark.__tests__.test_utilities import (
    ensure_enough_node_funds,
    wait_for_payment_completion,
)

log = logging.getLogger("python_sdk_test_regtest_client_withdrawal")

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


# Create test invoice from routing node and pay it from node 1.
def test_withdraw_from_node1() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    ensure_enough_node_funds(client, LIGHTSPARK_RS_NODE_ID, 50_000)
    invoice = client.create_test_mode_invoice(LIGHTSPARK_RS_NODE_ID, 50_000)
    seed_bytes = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED)
    client.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID,
        seed_bytes,
        lightspark.BitcoinNetwork.REGTEST,
    )
    payment = client.pay_invoice(LIGHTSPARK_RS_NODE_ID, invoice, 60, 10_000, None)
    tx = wait_for_payment_completion(client, payment.id)
    assert isinstance(tx, lightspark.OutgoingPayment)
    assert (
        tx.status != lightspark.TransactionStatus.FAILED
    ), f"Payment failed: {tx.failure_reason.name if tx.failure_reason else 'Failure reason unavailable'}"
    log.info(tx)
    log.info("===test_withdraw_from_node1===SUCCEEDED\n")


# Create test invoice from routing node and pay it from node 2.
def test_withdraw_from_node2() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID_2,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    ensure_enough_node_funds(client, LIGHTSPARK_RS_NODE_ID_2, 50_000)
    invoice = client.create_test_mode_invoice(LIGHTSPARK_RS_NODE_ID_2, 50_000)
    seed_bytes = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED_2)
    client.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID_2,
        seed_bytes,
        lightspark.BitcoinNetwork.REGTEST,
    )
    payment = client.pay_invoice(LIGHTSPARK_RS_NODE_ID_2, invoice, 60, 10_000, None)
    tx = wait_for_payment_completion(client, payment.id)
    assert isinstance(tx, lightspark.OutgoingPayment)
    assert (
        tx.status != lightspark.TransactionStatus.FAILED
    ), f"Payment failed: {tx.failure_reason.name if tx.failure_reason else 'Failure reason unavailable'}"
    log.info(tx)
    log.info("===test_withdraw_from_node2===SUCCEEDED\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    test_withdraw_from_node1()
    test_withdraw_from_node2()
