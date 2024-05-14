# Changelog

# v2.7.1

- Minor type fix in the `outgoing_payments_for_payment_hash` query.

# v2.7.0

- Add `fail_htlcs` function to cancel pending htlcs (for example for HODL invoices).
- Add `outgoing_payments_for_payment_hash` to get all outgoing payments for a specific hash.
- Compress requests and support zstd.

# v2.6.0

- Use a 64-bit nonce for signed requests to avoid conflicts.
- Add `is_internal_payment` fields to payment objects.
- Add `multisig_wallet_address_validation_parameters` to support validating node wallet addresses used for deposits.
- Add `incoming_payments_for_invoice` to get all incoming payments for an invoice.

# v2.5.1

- Ensure that the README and LICENSE are included in the pypi package.
- Make get_decoded_payment_request return an InvoiceData type.

# v2.5.0

- Add is_uma flag to payment objects. Note that this is only accurate for payments/invoices created with create_uma_invoice or pay_uma_invoice.
- Tweak the ChannelSnapshot object to make it more expressive.
- Include type info in the package release.

# v2.4.2
- Update dependencies.

# v2.4.1
- Update dependencies.

# v2.4.0

- Add a function for cancelling unpaid invoices.
- Add UMA invites support.

# v2.3.0

- Add the Balances object to wallets and nodes for a more human-readable view of balances.

# v2.2.0

- Add a call to get outgoing payments for an invoice.

# v2.1.3

- Add webhook handling example and fix create_test_mode_payment bug.

# v2.1.2

- Fix a signing key bug.

# v2.1.1

- Update dependencies.

# v2.1.0

- Remove UMA from lightspark SDK. Go install from https://pypi.org/project/uma-sdk/ instead.

# v2.0.0

- Add support for remote signing.

# v1.4.4

- Fix parsing of the pay_uma_invoice response

# v1.4.3

- Fix a few UMA bugs/ommisions:
  - Add expiry_secs to invoice calls
  - Parse create_uma_invoice correctly
  - Add fees to the invoice amount

# v1.4.2

- Fix a packaging problem with UMA.

# v1.4.1

- Fix deserializing nullable lists

# v1.4.0

- Adding UMA protocol support
- Adding some compliance-related client functions to support UMA

# v1.3.0

- Add invoice expirySecs to the invoice creation functions
- Return Invoice object instead of InvoiceData so that you can store the Invoice ID if needed
- Lots of docs improvements
- Allow fetching transactions and invoices for a wallet tied to the current account.

# v1.2.0

- Adding 2 new functions for test mode:
  - `create_test_mode_invoice` which can give you an encoded lightning invoice that can be paid from your test wallet via the payInvoice function
  - `create_test_mode_payment` to pay an invoice created from your test wallet via createInvoice

# v1.1.0

- Adding the ability to manage wallets tied to the current account. See `Account.get_wallets()` and the `Wallet` object.

# v1.0.0

- Added ability to create amp invoice.
- Fixed request_withdrawal.

# v0.9.1

Fixed a bug with paying invoices without specifying amount_msats.

# v0.9.0

Early beta preview of what will be our 1.0.0 release API. This is a major breaking change from the previous version of the SDK with a cleaner API surface and some nice new feature improvements from early feedback.

# v0.5.1

## New Features:

- Added a `commit_fee` field to the channel object to get the amount to be paid in fees for the current set of commitment transactions.

# v0.5.0

Several breaking changes and improvements to the SDK to make it more robust and easier to use.

## Breaking Changes:

- `Edge` objects' entites have been collapsed into `Connection` objects to remove the need for the client to manaually pull out entities from the `edges` field.

  **Before:**

  ```python
  for edge in account.get_transactions().edges:
      print(edge.entity.amount)
  ```

  **After:**

  ```python
  for transaction in account.get_transactions().entities:
      print(transaction.amount)
  ```

- Removed several queries and types which are not needed in the 3P SDK and shouldn't have been exposed. If you were using any of these, please let us know!

## New Features:

- `LightsparkClient.fund_node` to automatically add fake funds to a REGTEST node.
- `LightsparkClient.create_api_token` and `LightsparkClient.delete_api_token` to create and delete API tokens.
- `LightsparkClient.send_payment` to send a keysend payment using a destination node's public key which doesn't require an invoice at all.

## Notable fixes:

- Adding a `__FUTURE_VALUE__` value to all enum classes. This allows the SDK to be forward-compatible with new values that may be added to the API in the future, rather than crashing.

# v0.4.3

- Fix instantiation of enums (they were instantiated as `str` objects)
- Return concrete entities instead of interfaces. This fixes the fact that `Account.get_transactions` did not return all the transactions details.
  - Spread fragments on GraphQL interfaces to enable fetching the details of each entity.
  - Conditional JSON loaders to instantiate the right concrete object.
- Add `__init__.py` files for better module support.
- Add `setup.py` for PIP repository support.

# v0.4.2

- Adds a way to paginate transactions (and other connections) using `after`.
- Updates the SDK to match the latest API version (some fields were added, no breaking change)

# v0.4.1

- Fix 2 bugs around `datetime` serialization:
  - Add the serialization to the JSON encoder
  - Make sure the `datetime` objects are timezone aware

# v0.4.0

- Fields that take arguments are now fetched lazily and expose a function for the client to specify the arguments. Impacts the following fields:
  - `Account.blockchain_balance`
  - `Account.conductivity`
  - `Account.local_balance`
  - `Account.remote_balance`
  - `Account.uptime_percentage`
  - `Channel.uptime_percentage`

```python
# Old way to query (example)
account.blockchain_balance

# New way to query (examples)
account.get_blockchain_balance()
account.get_blockchain_balance(bitcoin_networks=[lightspark.BitcoinNetwork.REGTEST])
```

# v0.3.0

- Eagerly fetch `InvoiceData.destination`

# v0.2.0

SDK and APIs completely refactored. Consider this a new version

# v0.1.0

First draft of the SDK.
