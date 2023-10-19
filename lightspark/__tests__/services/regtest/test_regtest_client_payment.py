import logging

import lightspark
from lightspark.__tests__.test_config import *
from lightspark.__tests__.test_utilities import (
    ensure_enough_node_funds,
    wait_for_payment_completion,
)

log = logging.getLogger("python_sdk_test_regtest_client_payment")


# Create an invoice from node 1, pay it from node 2
def test_pay_invoice_node2_to_node1() -> None:
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    invoice = client.create_invoice(LIGHTSPARK_RS_NODE_ID, 10_000_000)
    log.info(invoice)

    client2 = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID_2,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    ensure_enough_node_funds(client2, LIGHTSPARK_RS_NODE_ID_2, 10_000_000)
    seed_bytes2 = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED_2)
    client2.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID_2,
        seed_bytes2,
        lightspark.BitcoinNetwork.REGTEST,
    )
    payment = client2.pay_invoice(
        LIGHTSPARK_RS_NODE_ID_2,
        invoice.data.encoded_payment_request,
        60,
        int(10_000_000 * 0.16),
        None,
    )
    tx = wait_for_payment_completion(client2, payment.id)
    assert isinstance(tx, lightspark.OutgoingPayment)
    assert (
        tx.status != lightspark.TransactionStatus.FAILED
    ), f"Payment failed: {tx.failure_reason.name if tx.failure_reason else 'Failure reason unavailable'}"
    log.info(tx)
    log.info("===test_pay_invoice_node2_to_node1===SUCCEEDED\n")


#  Create an invoice from node 2, pay it from node 1
def test_pay_invoice_node1_to_node2() -> None:
    client2 = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID_2,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET_2,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    invoice = client2.create_invoice(LIGHTSPARK_RS_NODE_ID_2, 10_000_000)
    log.info(invoice)

    client = lightspark.LightsparkSyncClient(
        api_token_client_id=LIGHTSPARK_API_TOKEN_CLIENT_ID,
        api_token_client_secret=LIGHTSPARK_API_TOKEN_CLIENT_SECRET,
        base_url=LIGHTSPARK_API_ENDPOINT,
    )
    ensure_enough_node_funds(client, LIGHTSPARK_RS_NODE_ID, 10_000_000)
    seed_bytes = bytes.fromhex(LIGHTSPARK_RS_MASTER_SEED)
    client.provide_node_master_seed(
        LIGHTSPARK_RS_NODE_ID,
        seed_bytes,
        lightspark.BitcoinNetwork.REGTEST,
    )
    payment = client.pay_invoice(
        LIGHTSPARK_RS_NODE_ID,
        invoice.data.encoded_payment_request,
        60,
        int(10_000_000 * 0.16),
        None,
    )
    tx = wait_for_payment_completion(client, payment.id)
    assert isinstance(tx, lightspark.OutgoingPayment)
    assert (
        tx.status != lightspark.TransactionStatus.FAILED
    ), f"Payment failed: {tx.failure_reason.name if tx.failure_reason else 'Failure reason unavailable'}"
    log.info(tx)
    log.info("===test_pay_invoice_node1_to_node2===SUCCEEDED\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    test_pay_invoice_node2_to_node1()
    test_pay_invoice_node1_to_node2()
