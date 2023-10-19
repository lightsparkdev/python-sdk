import logging

import lightspark
from lightspark.__tests__.test_config import *
from lightspark.__tests__.test_utilities import wait_for_payment_completion

log = logging.getLogger("python_sdk_test_regtest_client_funding")


# Create invoice for node 1 and pay it from routing node. You'll need to run this a few
# times the first time you are funding a node to get enough funds in.
# Note: This will only work with REGTEST nodes.
def test_funding_node1() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    invoice = client.create_invoice(LIGHTSPARK_RS_NODE_ID, 10_000_000)
    log.info("Created invoice: %s", invoice)
    seed_bytes = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED)
    client.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID, seed_bytes, lightspark.BitcoinNetwork.REGTEST
    )
    payment = client.create_test_mode_payment(
        LIGHTSPARK_RS_NODE_ID, invoice.data.encoded_payment_request
    )
    log.info("Created payment: %s", payment)
    tx = wait_for_payment_completion(client, payment.id)
    assert tx.status != lightspark.TransactionStatus.FAILED, "Payment failed!"
    log.info(tx)
    log.info("===test_funding_node1===SUCCEEDED\n")


# Create invoice for node 2 and pay it from routing node. You'll need to run this a few
# times the first time you are funding a node to get enough funds in.
# Note: This will only work with REGTEST nodes.
def test_funding_node2() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID_2,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    invoice = client.create_invoice(LIGHTSPARK_RS_NODE_ID_2, 10_000_000)
    log.info("Created invoice: %s", invoice)
    seed_bytes = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED_2)
    client.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID_2,
        seed_bytes,
        lightspark.BitcoinNetwork.REGTEST,
    )
    payment = client.create_test_mode_payment(
        LIGHTSPARK_RS_NODE_ID_2, invoice.data.encoded_payment_request
    )
    log.info("Created payment: %s", payment)
    tx = wait_for_payment_completion(client, payment.id)
    assert tx.status != lightspark.TransactionStatus.FAILED, "Payment failed!"
    log.info(tx)
    log.info("===test_funding_node2===SUCCEEDED\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    test_funding_node1()
    test_funding_node2()
