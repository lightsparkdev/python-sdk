#!/usr/bin/env python3
"""
Test Suite: Verify Security Fixes

This script tests the fixed implementations to ensure they properly
mitigate the identified vulnerabilities.
"""

import sys
import json
import hmac
import secrets
from datetime import datetime


def test_secure_hashing():
    """Test secure hashing implementation"""
    print("\n" + "=" * 70)
    print("TEST 1: Secure Hashing (UMA Identifiers & Phone Numbers)")
    print("=" * 70)
    
    from secure_hashing import SecureHasher
    
    # Initialize with secret key
    secret_key = secrets.token_bytes(32)
    hasher = SecureHasher(secret_key)
    
    print("\n[*] Testing UMA identifier hashing...")
    
    # Test 1: Same identifier should produce same hash
    identifier = "alice@example.com"
    signing_key = b"x" * 32
    
    hash1 = hasher.hash_uma_identifier(identifier, signing_key)
    hash2 = hasher.hash_uma_identifier(identifier, signing_key)
    
    if hash1 == hash2:
        print("  ✓ Deterministic hashing works (same input = same output)")
    else:
        print("  ✗ FAIL: Hashing is not deterministic")
        return False
    
    # Test 2: Different secret keys should produce different hashes
    hasher2 = SecureHasher(secrets.token_bytes(32))
    hash3 = hasher2.hash_uma_identifier(identifier, signing_key)
    
    if hash1 != hash3:
        print("  ✓ Different secret keys produce different hashes")
    else:
        print("  ✗ FAIL: Secret key not affecting hash")
        return False
    
    # Test 3: Hash verification
    is_valid = hasher.verify_uma_hash(identifier, signing_key, hash1)
    if is_valid:
        print("  ✓ Hash verification works correctly")
    else:
        print("  ✗ FAIL: Hash verification failed")
        return False
    
    print("\n[*] Testing phone number hashing...")
    
    # Test 4: Phone number hashing
    phone = "+12125551234"
    phone_hash1 = hasher.hash_phone_number(phone)
    phone_hash2 = hasher.hash_phone_number(phone)
    
    if phone_hash1 == phone_hash2:
        print("  ✓ Phone number hashing is deterministic")
    else:
        print("  ✗ FAIL: Phone hashing not deterministic")
        return False
    
    # Test 5: Different phones produce different hashes
    phone2 = "+13105559999"
    phone_hash3 = hasher.hash_phone_number(phone2)
    
    if phone_hash1 != phone_hash3:
        print("  ✓ Different phone numbers produce different hashes")
    else:
        print("  ✗ FAIL: Hash collision detected")
        return False
    
    # Test 6: Invalid phone number format
    try:
        hasher.hash_phone_number("not-a-phone")
        print("  ✗ FAIL: Invalid phone number accepted")
        return False
    except ValueError:
        print("  ✓ Invalid phone number format rejected")
    
    print("\n[✓] All secure hashing tests passed!")
    return True


def test_secure_webhooks():
    """Test secure webhook parsing"""
    print("\n" + "=" * 70)
    print("TEST 2: Secure Webhook Parsing")
    print("=" * 70)
    
    from secure_webhooks import WebhookEvent, WebhookValidationError
    
    webhook_secret = "test_secret_key"
    
    print("\n[*] Testing valid webhook...")
    
    # Test 1: Valid webhook
    valid_payload = {
        "event_type": "PAYMENT_FINISHED",
        "event_id": "evt_123",
        "timestamp": "2026-01-18T13:00:00+00:00",
        "entity_id": "entity_456",
        "wallet_id": "wallet_789"
    }
    
    data = json.dumps(valid_payload).encode('utf-8')
    mac = hmac.new(webhook_secret.encode("ascii"), msg=data, digestmod="sha256")
    signature = mac.digest().hex()
    
    try:
        event = WebhookEvent.verify_and_parse(data, signature, webhook_secret)
        print(f"  ✓ Valid webhook parsed successfully")
        print(f"    Event: {event.event_type.value}, ID: {event.event_id}")
    except Exception as e:
        print(f"  ✗ FAIL: Valid webhook rejected: {e}")
        return False
    
    print("\n[*] Testing invalid signature...")
    
    # Test 2: Invalid signature
    try:
        WebhookEvent.verify_and_parse(data, "invalid_signature", webhook_secret)
        print("  ✗ FAIL: Invalid signature accepted")
        return False
    except ValueError:
        print("  ✓ Invalid signature rejected")
    
    print("\n[*] Testing missing required fields...")
    
    # Test 3: Missing required field
    invalid_payload = {
        "event_type": "PAYMENT_FINISHED",
        # Missing event_id
        "timestamp": "2026-01-18T13:00:00+00:00",
        "entity_id": "entity_456"
    }
    
    data = json.dumps(invalid_payload).encode('utf-8')
    
    try:
        WebhookEvent.parse(data)
        print("  ✗ FAIL: Missing field accepted")
        return False
    except WebhookValidationError as e:
        print(f"  ✓ Missing field rejected: {e}")
    
    print("\n[*] Testing invalid event type...")
    
    # Test 4: Invalid event type
    invalid_payload = {
        "event_type": "INVALID_TYPE",
        "event_id": "evt_123",
        "timestamp": "2026-01-18T13:00:00+00:00",
        "entity_id": "entity_456"
    }
    
    data = json.dumps(invalid_payload).encode('utf-8')
    
    try:
        WebhookEvent.parse(data)
        print("  ✗ FAIL: Invalid event type accepted")
        return False
    except WebhookValidationError:
        print("  ✓ Invalid event type rejected")
    
    print("\n[*] Testing oversized payload...")
    
    # Test 5: Oversized payload
    large_payload = {
        "event_type": "PAYMENT_FINISHED",
        "event_id": "evt_123",
        "timestamp": "2026-01-18T13:00:00+00:00",
        "entity_id": "entity_456",
        "extra": "A" * (2 * 1024 * 1024)  # 2MB
    }
    
    data = json.dumps(large_payload).encode('utf-8')
    
    try:
        WebhookEvent.parse(data)
        print("  ✗ FAIL: Oversized payload accepted")
        return False
    except WebhookValidationError:
        print("  ✓ Oversized payload rejected")
    
    print("\n[*] Testing malformed JSON...")
    
    # Test 6: Malformed JSON
    try:
        WebhookEvent.parse(b'{"invalid": json}')
        print("  ✗ FAIL: Malformed JSON accepted")
        return False
    except WebhookValidationError:
        print("  ✓ Malformed JSON rejected")
    
    print("\n[✓] All webhook validation tests passed!")
    return True


def run_all_tests():
    """Run all security tests"""
    print("=" * 70)
    print("SECURITY FIXES VERIFICATION TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Test 1: Secure hashing
    results.append(("Secure Hashing", test_secure_hashing()))
    
    # Test 2: Secure webhooks
    results.append(("Secure Webhooks", test_secure_webhooks()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name:30s} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED - Security fixes verified!")
    else:
        print("SOME TESTS FAILED - Review implementation")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
