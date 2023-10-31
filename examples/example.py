# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import logging
import os
from datetime import datetime, timedelta

import lightspark

logger = logging.getLogger("lightspark")
logger.setLevel(logging.DEBUG)

#################################################################
## MODIFY THOSE VARIABLES BEFORE RUNNING THE EXAMPLE
#################################################################
##
## We defined those variables as environment variables, but if you are just
## running the example locally, feel free to just set the values in Python.
##
## First, initialize your client ID and client secret. Those are available
## in your account at https://app.lightspark.com/api_config
api_token_client_id = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_ID")
api_token_client_secret = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_SECRET")

node_password = os.environ.get("LIGHTSPARK_TEST_NODE_PASSWORD")

# Let's start by creating a client

assert api_token_client_secret
assert api_token_client_id
assert node_password

client = lightspark.LightsparkSyncClient(
    api_token_client_id=api_token_client_id,
    api_token_client_secret=api_token_client_secret,
    base_url=os.environ.get("LIGHTSPARK_EXAMPLE_BASE_URL"),
)

# Get some fee estimates for Bitcoin (L1) transactions

fee_estimate = client.get_bitcoin_fee_estimate(
    bitcoin_network=lightspark.BitcoinNetwork.REGTEST
)
print(
    f"Fees for a fast transaction {fee_estimate.fee_fast.preferred_currency_value_approx} {fee_estimate.fee_fast.preferred_currency_unit}."
)
print(
    f"Fees for a cheap transaction {fee_estimate.fee_min.preferred_currency_value_approx} {fee_estimate.fee_min.preferred_currency_unit}."
)
print("")

# List your account's lightning nodes

account = client.get_current_account()
print(f"Your account name is {account.name}.")
print("")


api_tokens_connection = account.get_api_tokens()
print(f"You initially have {str(api_tokens_connection.count)} active API tokens.")
print("")

(api_token, client_secret) = client.create_api_token(name="Test token", test_mode=True)
print(f"Created API token {api_token.id}.")

api_tokens_connection = account.get_api_tokens()
print(f"You now have {str(api_tokens_connection.count)} active API tokens.")
print("")

client.delete_api_token(api_token_id=api_token.id)
print(f"Deleted API token {api_token.id}.")

api_tokens_connection = account.get_api_tokens()
print(f"You now have {str(api_tokens_connection.count)} active API tokens.")
print("")

# Check our account's conductivity on REGTEST

print(
    f"Your account's conductivity on REGTEST is {account.get_conductivity(bitcoin_networks=[lightspark.BitcoinNetwork.REGTEST])}/10."
)
print("")

# Check your account's local and remote balances for REGTEST
local_balance = account.get_local_balance(
    bitcoin_networks=[lightspark.BitcoinNetwork.REGTEST]
)
remote_balance = account.get_remote_balance(
    bitcoin_networks=[lightspark.BitcoinNetwork.REGTEST]
)
if local_balance and remote_balance:
    print(
        f"Your local balance is {local_balance.preferred_currency_value_approx} {local_balance.preferred_currency_unit}, your remote balance is {remote_balance.preferred_currency_value_approx} {remote_balance.preferred_currency_unit}."
    )

nodes_connection = account.get_nodes(
    first=50, bitcoin_networks=[lightspark.BitcoinNetwork.REGTEST]
)
if nodes_connection is None:
    raise Exception("Unable to fetch the nodes.")

print(f"You have {nodes_connection.count} nodes.")

node_id = None
node_name = None

for node in nodes_connection.entities:
    node_id = node.id
    node_name = node.display_name
print("")

assert node_id is not None
assert node_name is not None

# List the transactions for our account

transactions_connection = account.get_transactions(
    first=50, bitcoin_network=lightspark.BitcoinNetwork.REGTEST
)
print(
    f"There is a total of {transactions_connection.count} transaction(s) on this account:"
)
deposit_transaction_id = None
for transaction in transactions_connection.entities:
    print(
        f"    - {transaction.typename} at {str(transaction.created_at)}: {transaction.amount.preferred_currency_value_approx} {transaction.amount.preferred_currency_unit.name} ({transaction.status.name})"
    )
    if transaction.typename == "Deposit":
        deposit_transaction_id = transaction.id

    fees = None
    if (
        isinstance(transaction, lightspark.OutgoingPayment)
        or isinstance(transaction, lightspark.Withdrawal)
        or isinstance(transaction, lightspark.Deposit)
        or isinstance(transaction, lightspark.ChannelOpeningTransaction)
        or isinstance(transaction, lightspark.ChannelClosingTransaction)
    ):
        fees = transaction.fees
        if fees:
            print(
                f"        Paid {fees.preferred_currency_value_approx} {fees.preferred_currency_unit.name} in fees."
            )
print("")

# Fetch transactions using pagination
page_size = 10
iterations = 0
has_next = True
after = None
while has_next and iterations < 30:
    iterations += 1
    transactions_connection = account.get_transactions(
        first=page_size, bitcoin_network=lightspark.BitcoinNetwork.REGTEST, after=after
    )
    num = len(transactions_connection.entities)
    print(f"We got {num} transactions for the page (iteration #{iterations})")
    if transactions_connection.page_info.has_next_page:
        has_next = True
        after = transactions_connection.page_info.end_cursor
        print("  And we have another page!")
    else:
        has_next = False
        print("  And we're done!")
print("")


# Get the transactions that happened in the past day on REGTEST

transactions_connection = account.get_transactions(
    bitcoin_network=lightspark.BitcoinNetwork.REGTEST,
    after_date=datetime.now() - timedelta(hours=24),
)
print(f"We had {transactions_connection.count} transactions in the past 24 hours.")

# Get details for a transaction

assert deposit_transaction_id is not None
deposit = client.get_entity(deposit_transaction_id, lightspark.Deposit)
print("Details of deposit transaction")
print(deposit)
print("")

# Generate a payment request

invoice = client.create_invoice(
    node_id=node_id,
    amount_msats=42000,
    memo="Pizza!",
)
print(f"Invoice created from {node_name}:")
print(f"Encoded invoice = {invoice.data.encoded_payment_request}")
print("")

# Decode the payment request
decoded_request = client.get_decoded_payment_request(
    encoded_payment_request=invoice.data.encoded_payment_request
)
assert isinstance(decoded_request, lightspark.InvoiceData)
print("Decoded payment request:")
print("    destination_public_key = " + str(decoded_request.destination.public_key))
print(
    "    amount = "
    + str(decoded_request.amount.preferred_currency_value_approx)
    + " "
    + str(decoded_request.amount.preferred_currency_unit.name)
)
print("    memo = " + str(decoded_request.memo))
print("")

# Let's simulate a payment to the invoice just created

# First, we need to recover the signing key.
client.recover_node_signing_key(node_id=node_id, node_password=node_password)
print(f"{node_name}'s signing key has been loaded.")
print("")

# Simulate a payment from other node to my generated invoice
payment = client.create_test_mode_payment(
    local_node_id=node_id,
    encoded_invoice=invoice.data.encoded_payment_request,
)
print(f"Simulated payment to the invoice done with ID = {payment.id}")
print("")

# Pay invoice sample
#
test_invoice = client.create_test_mode_invoice(
    local_node_id=node_id,
    amount_msats=42000,
    memo="Pizza!",
)
print(f"Test invoice created: {test_invoice}")
print("")
payment = client.pay_invoice(
    node_id=node_id,
    encoded_invoice=test_invoice,  # replace test_invoice with real encoded invoice in non-test mode
    timeout_secs=60,
    maximum_fees_msats=500,
)
print(f"Payment to the invoice done with ID = {payment.id}")
print("")

outgoing_payments = client.outgoing_payments_for_invoice(
    encoded_invoice=test_invoice,  # replace test_invoice with real encoded invoice in non-test mode
)
print(f"Outgoing payments for invoice {test_invoice}:")
for outgoing_payment in outgoing_payments:
    print(f"    - {outgoing_payment.id}")
print("")

# Key Send sample
#
# payment = client.send_payment(
#     node_id=node_id,
#     destination_public_key=<public key>,
#     amount_msats=2000,
#     timeout_secs=60,
#     maximum_fees_msats=500,
# )
# print(f"Payment directly to node without invoice done with ID = {payment.id}")
# print("")

# Get a wallet address
address = client.create_node_wallet_address(node_id=node_id)
print(f"Got a bitcoin address for {node_name}: {address}")
print("")

# Withdraw funds!
# TODO: Uncomment when withrawals are working again.
# withdrawal = client.request_withdrawal(
#     node_id=node_id,
#     amount_sats=1000,
#     bitcoin_address=address,
#     withdrawal_mode=lightspark.WithdrawalMode.WALLET_THEN_CHANNELS,
# )
# print(f"Money was withdrawn with ID = {withdrawal.id}")
# print("")

# Fetch the channels for Node 1
node = client.get_entity(
    node_id,
    lightspark.LightsparkNode,
)
if node is None:
    raise Exception("Couldn't find node!")

channels_connection = node.get_channels(first=10)
print(f"{node_name} has {channels_connection.count} channel(s):")
for channel in channels_connection.entities:
    if channel.remote_node_id:
        remote_node = client.get_entity(channel.remote_node_id, lightspark.Node)
        alias = remote_node.alias if remote_node else "UNKNOWN"
        if channel.local_balance and channel.remote_balance:
            print(
                f"    - With {alias}. Local/remote balance = {channel.local_balance.preferred_currency_value_approx} {channel.local_balance.preferred_currency_unit}/{channel.remote_balance.preferred_currency_value_approx} {channel.remote_balance.preferred_currency_unit}"
            )
print("")

# Screen a node
node_pubkey = "bc1qj4mfcgej3wxp8eundzq7sq8f80wps02kk38sgadrer39mr5l7ncqrgmp89"
rating = client.screen_node(
    provider=lightspark.ComplianceProvider.CHAINALYSIS, node_pubkey=node_pubkey
)
print(f"Got risk rating for node with pubkey {node_pubkey}: {rating}")
print("")

# Register a successful payment
node_pubkey = "bc1qj4mfcgej3wxp8eundzq7sq8f80wps02kk38sgadrer39mr5l7ncqrgmp89"
payment_id = "<Your successful outgoing payment id>"
client.register_payment(
    provider=lightspark.ComplianceProvider.CHAINALYSIS,
    node_pubkey=node_pubkey,
    payment_id=payment_id,
    direction=lightspark.PaymentDirection.SENT,
)
print(f"Successfully registered payment {payment_id}")
print("")

# Issue an arbitrary GraphQL request

result = client.execute_graphql_request(
    document="""
query Test($networks: [BitcoinNetwork!]!) {
    current_account {
        name
        nodes(bitcoin_networks: $networks) {
            count
        }
    }
}
""",
    variables={"networks": [lightspark.BitcoinNetwork.REGTEST]},
)

name = result["current_account"]["name"]
count = result["current_account"]["nodes"]["count"]
print(f"The account {name} has {count} nodes on the REGTEST network.")
