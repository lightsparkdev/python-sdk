import logging
import time
from typing import Optional, TypeVar

import lightspark

log = logging.getLogger("python-sdk_test_utils")

T = TypeVar("T")
TIME_OUT_DURATION_SEC = 180


def none_throws(value: Optional[T], error_message: Optional[str] = None) -> T:
    if value is None:
        raise Exception(error_message or "Unexpected None")
    return value


def wait_for_payment_completion(
    client: lightspark.LightsparkSyncClient, payment_id: str
) -> lightspark.LightningTransaction:
    payment = none_throws(
        client.get_entity(payment_id, lightspark.LightningTransaction)
    )
    startTime = time.time()
    while payment.status not in {
        lightspark.TransactionStatus.SUCCESS,
        lightspark.TransactionStatus.FAILED,
    }:
        if time.time() - startTime > TIME_OUT_DURATION_SEC:
            log.error("Payment timed out: %s", payment.id)
            return payment
        payment = none_throws(
            client.get_entity(payment_id, lightspark.LightningTransaction)
        )
    log.info(
        "The payment status takes %s seconds to be updated.", time.time() - startTime
    )
    return payment


# Ensure node has enough funds to pay the invoice.
# If not, create an invoice from the routing node and pay it from the node.
# This will only work with REGTEST nodes.
def ensure_enough_node_funds(
    client: lightspark.LightsparkSyncClient, node_id: str, amount_msats: int
) -> None:
    node = none_throws(client.get_entity(node_id, lightspark.LightsparkNode))
    if not node.local_balance:
        raise Exception(f"Node id, {node.id}, has no local balance.")
    balance_msats = node.local_balance.convert_to(
        lightspark.CurrencyUnit.MILLISATOSHI
    ).preferred_currency_value_rounded
    log.info(
        "Check if node id, %s, has enough local balance as of, %s msats, to send, %s msats, before funding.",
        node.id,
        balance_msats,
        amount_msats,
    )
    if balance_msats < amount_msats:
        invoice = client.create_invoice(node.id, amount_msats * 5, None, None, None)
        payment = client.create_test_mode_payment(
            node.id, invoice.data.encoded_payment_request, None
        )
        wait_for_payment_completion(client, payment.id)
        startTime = time.time()
        while True:
            node = none_throws(client.get_entity(node_id, lightspark.LightsparkNode))
            if not node.local_balance:
                raise Exception(f"Node id, {node.id}, has no local balance.")
            balance_msats = node.local_balance.convert_to(
                lightspark.CurrencyUnit.MILLISATOSHI
            ).preferred_currency_value_rounded
            log.info(
                "Check if node id, %s, has enough local balance as of, %s msats, to send, %s msats, after funding.",
                node.id,
                balance_msats,
                amount_msats,
            )
            if balance_msats >= amount_msats:
                break
            if time.time() - startTime > TIME_OUT_DURATION_SEC:
                raise Exception(
                    "Funding node id, %s, failed, it still has %s msats balance.",
                    node.id,
                    balance_msats,
                )

        log.info(
            "It takes %s seconds for the node's local balance to be updated.",
            time.time() - startTime,
        )
