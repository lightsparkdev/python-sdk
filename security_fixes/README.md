# Security Fixes for Lightspark Python SDK

This directory contains security fixes and proof-of-concept exploits for 3 medium severity vulnerabilities identified in the Lightspark Python SDK.

## 📋 Contents

### Proof of Concept Exploits

1. **`poc_timing_attack.py`** - Demonstrates timing attack on UMA identifier hashing
2. **`poc_phone_enumeration.py`** - Demonstrates phone number enumeration via rainbow tables
3. **`poc_webhook_exploit.py`** - Demonstrates webhook input validation exploits

### Fixed Implementations

1. **`secure_hashing.py`** - Fixed UMA identifier and phone number hashing using HMAC-SHA256
2. **`secure_webhooks.py`** - Fixed webhook parsing with comprehensive validation
3. **`test_fixes.py`** - Test suite to verify security fixes

## 🚀 Quick Start

### Running the PoC Exploits

```bash
# Navigate to the security_fixes directory
cd security_fixes

# Run PoC #1: Timing Attack
python poc_timing_attack.py

# Run PoC #2: Phone Number Enumeration
python poc_phone_enumeration.py

# Run PoC #3: Webhook Validation Exploit
python poc_webhook_exploit.py
```

### Testing the Fixes

```bash
# Run the test suite
python test_fixes.py
```

## 🔒 Vulnerabilities Fixed

### 1. Timing Attack in UMA Identifier Hashing (MEDIUM)

**Vulnerability:** The original `hash_uma_identifier()` function used plain SHA256, making it vulnerable to timing attacks and correlation attacks.

**Fix:** 
- Replaced SHA256 with HMAC-SHA256
- Added secret key requirement
- Uses constant-time comparison via `hmac.compare_digest()`

**Before:**
```python
def hash_uma_identifier(self, identifier: str, signing_private_key: bytes) -> str:
    now = datetime.now(timezone.utc)
    input_data = identifier + f"{now.month}-{now.year}" + signing_private_key.hex()
    return sha256(input_data.encode()).hexdigest()
```

**After:**
```python
def hash_uma_identifier(self, identifier: str, signing_private_key: bytes) -> str:
    # ... (input preparation)
    hash_value = hmac.digest(
        self.secret_key,
        input_data.encode('utf-8'),
        hashlib.sha256
    )
    return hash_value.hex()
```

### 2. Phone Number Enumeration (MEDIUM)

**Vulnerability:** Phone numbers were hashed using unsalted SHA256, enabling rainbow table attacks.

**Fix:**
- Replaced SHA256 with HMAC-SHA256
- Added secret key to prevent precomputation
- Added E.164 format validation

**Before:**
```python
def _hash_phone_number(self, phone_number_e164_format: str) -> str:
    return sha256(phone_number_e164_format.encode()).hexdigest()
```

**After:**
```python
def hash_phone_number(self, phone_number_e164: str) -> str:
    # Validate E.164 format
    if not E164_REGEX.match(phone_number_e164):
        raise ValueError("Phone number must be in E.164 format")
    
    hash_value = hmac.digest(
        self.secret_key,
        phone_number_e164.encode('utf-8'),
        hashlib.sha256
    )
    return hash_value.hex()
```

### 3. Webhook Input Validation (MEDIUM)

**Vulnerability:** Webhook parsing lacked comprehensive validation, enabling DoS and information disclosure.

**Fix:**
- Added field existence validation
- Added type validation for all fields
- Added size limits (1MB max payload)
- Sanitized error messages
- Added schema validation

**Before:**
```python
@classmethod
def parse(cls, data: bytes) -> "WebhookEvent":
    event = json.loads(data.decode("utf-8"))
    return cls(
        event_type=WebhookEventType[event["event_type"]],  # Can throw KeyError
        event_id=event["event_id"],  # Can throw KeyError
        # ...
    )
```

**After:**
```python
@classmethod
def parse(cls, data: bytes) -> "WebhookEvent":
    # Size validation
    if len(data) > cls.MAX_PAYLOAD_SIZE:
        raise WebhookValidationError("Payload too large")
    
    # Parse with error handling
    try:
        event = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise WebhookValidationError(f"Invalid JSON at position {e.pos}")
    
    # Validate required fields exist
    required_fields = ["event_type", "event_id", "timestamp", "entity_id"]
    missing_fields = [f for f in required_fields if f not in event]
    if missing_fields:
        raise WebhookValidationError(f"Missing fields: {', '.join(missing_fields)}")
    
    # Validate and parse each field with type checking
    # ...
```

## 📊 PoC Demonstrations

### PoC #1: Timing Attack

Demonstrates how timing differences can reveal if two UMA identifiers are the same, breaking user anonymity.

**Output:**
```
[!] VULNERABILITY: The hash is deterministic and predictable!
[!] An attacker can:
    1. Precompute hashes for known identifiers
    2. Compare transaction hashes to identify users
    3. Track users across multiple transactions
```

### PoC #2: Phone Number Enumeration

Demonstrates building a rainbow table to reverse phone number hashes.

**Output:**
```
[+] Rainbow table generated: 50,000 entries in 0.45s
[+] Rate: 111,111 hashes/second

Hash: 8f3d2e1a...
  ✓ CRACKED! Phone number: +12125551234
```

### PoC #3: Webhook Validation Exploit

Demonstrates various attacks on webhook parsing including DoS and information disclosure.

**Output:**
```
[*] Testing: Exploit #1 - Missing 'event_id' field
    ✗ KeyError: 'event_id'
    [!] VULNERABILITY: Missing field causes exception
    [!] Information disclosed: Field name 'event_id'
```

## 🔧 Integration Guide

### Using Secure Hashing

```python
from secure_hashing import SecureHasher
import os

# Initialize with secret key from environment
secret_key = os.environ.get('HASH_SECRET_KEY').encode()
hasher = SecureHasher(secret_key)

# Hash UMA identifier
uma_hash = hasher.hash_uma_identifier(
    identifier="alice@example.com",
    signing_private_key=signing_key
)

# Hash phone number
phone_hash = hasher.hash_phone_number("+12125551234")

# Verify hashes (constant-time)
is_valid = hasher.verify_uma_hash(identifier, signing_key, uma_hash)
```

### Using Secure Webhooks

```python
from secure_webhooks import WebhookEvent, WebhookValidationError

try:
    event = WebhookEvent.verify_and_parse(
        data=request.data,
        hex_digest=request.headers.get("lightspark-signature"),
        webhook_secret=WEBHOOK_SECRET
    )
    # Process valid webhook
    print(f"Event: {event.event_type.value}")
except WebhookValidationError as e:
    # Handle validation error
    return {"error": "Invalid webhook"}, 400
except ValueError as e:
    # Handle signature verification error
    return {"error": "Invalid signature"}, 401
```

## ⚠️ Breaking Changes

These fixes introduce breaking changes:

1. **`hash_uma_identifier()` now requires initialization with `secret_key`**
   - Existing code must be updated to provide a secret key
   - Existing hashes will not match (migration required)

2. **`hash_phone_number()` now requires initialization with `secret_key`**
   - Existing code must be updated to provide a secret key
   - Existing hashes will not match (migration required)

3. **Webhook parsing now raises `WebhookValidationError`**
   - Code must handle the new exception type
   - Error messages are sanitized (less verbose)

## 🔐 Security Recommendations

1. **Secret Key Management**
   - Generate a strong 32-byte secret key: `secrets.token_bytes(32)`
   - Store in environment variables or secure key management system
   - Rotate keys periodically
   - Never commit keys to version control

2. **Migration Strategy**
   - Plan for hash migration if upgrading existing systems
   - Consider maintaining both old and new hashes during transition
   - Update all clients before deprecating old hashes

3. **Monitoring**
   - Monitor for webhook validation errors
   - Alert on unusual patterns (potential attacks)
   - Log security events for audit trail

## 📝 License

These fixes are provided as security improvements for the Lightspark Python SDK.
