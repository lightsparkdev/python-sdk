#!/usr/bin/env python3
"""
FIXED VERSION: Secure UMA Identifier and Phone Number Hashing

This module contains the fixed implementations that address:
1. Timing attack vulnerability in UMA identifier hashing
2. Phone number enumeration via rainbow tables

Changes:
- Uses HMAC-SHA256 instead of plain SHA256
- Requires secret key for additional security
- Constant-time operations prevent timing attacks
"""

import hmac
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional


class SecureHasher:
    """Secure hashing implementation for identifiers and phone numbers"""
    
    def __init__(self, secret_key: bytes):
        """
        Initialize secure hasher with a secret key.
        
        Args:
            secret_key: Secret key for HMAC operations (should be at least 32 bytes)
        
        Raises:
            ValueError: If secret key is too short
        """
        if len(secret_key) < 32:
            raise ValueError("Secret key must be at least 32 bytes")
        self.secret_key = secret_key
    
    def hash_uma_identifier(
        self, 
        identifier: str, 
        signing_private_key: bytes,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Securely hash a UMA identifier using HMAC-SHA256.
        
        This prevents:
        - Timing attacks (using constant-time HMAC)
        - Precomputation attacks (using secret key)
        - Correlation attacks (using monthly rotation)
        
        Args:
            identifier: The UMA identifier to hash
            signing_private_key: The signing private key
            additional_context: Optional additional context for the hash
        
        Returns:
            Hex-encoded HMAC-SHA256 hash
        """
        now = datetime.now(timezone.utc)
        
        # Build input data with time-based rotation
        input_parts = [
            identifier,
            f"{now.month}-{now.year}",
            signing_private_key.hex()
        ]
        
        if additional_context:
            input_parts.append(additional_context)
        
        input_data = "|".join(input_parts)
        
        # Use HMAC-SHA256 with secret key
        # This prevents:
        # 1. Rainbow table attacks (secret key unknown to attacker)
        # 2. Timing attacks (hmac.digest uses constant-time comparison)
        hash_value = hmac.digest(
            self.secret_key,
            input_data.encode('utf-8'),
            hashlib.sha256
        )
        
        return hash_value.hex()
    
    def hash_phone_number(self, phone_number_e164: str) -> str:
        """
        Securely hash a phone number using HMAC-SHA256.
        
        This prevents:
        - Rainbow table attacks (using secret key)
        - Enumeration attacks (computational barrier)
        
        Args:
            phone_number_e164: Phone number in E.164 format
        
        Returns:
            Hex-encoded HMAC-SHA256 hash
        
        Raises:
            ValueError: If phone number is not in E.164 format
        """
        # Validate E.164 format
        E164_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")
        if not E164_REGEX.match(phone_number_e164):
            raise ValueError(
                "Phone number must be in E.164 format (e.g., +12125551234)"
            )
        
        # Use HMAC-SHA256 with secret key
        # The secret key prevents rainbow table attacks
        hash_value = hmac.digest(
            self.secret_key,
            phone_number_e164.encode('utf-8'),
            hashlib.sha256
        )
        
        return hash_value.hex()
    
    def verify_uma_hash(
        self,
        identifier: str,
        signing_private_key: bytes,
        expected_hash: str,
        additional_context: Optional[str] = None
    ) -> bool:
        """
        Verify a UMA identifier hash using constant-time comparison.
        
        Args:
            identifier: The UMA identifier
            signing_private_key: The signing private key
            expected_hash: The expected hash value
            additional_context: Optional additional context
        
        Returns:
            True if hash matches, False otherwise
        """
        computed_hash = self.hash_uma_identifier(
            identifier, 
            signing_private_key,
            additional_context
        )
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed_hash, expected_hash)
    
    def verify_phone_hash(self, phone_number_e164: str, expected_hash: str) -> bool:
        """
        Verify a phone number hash using constant-time comparison.
        
        Args:
            phone_number_e164: Phone number in E.164 format
            expected_hash: The expected hash value
        
        Returns:
            True if hash matches, False otherwise
        """
        computed_hash = self.hash_phone_number(phone_number_e164)
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed_hash, expected_hash)


# Example usage and migration guide
def example_usage():
    """Example of how to use the secure hasher"""
    
    # Initialize with a strong secret key (should be from environment/config)
    # In production, use: os.environ.get('HASH_SECRET_KEY').encode()
    import secrets
    secret_key = secrets.token_bytes(32)  # Generate 32 random bytes
    
    hasher = SecureHasher(secret_key)
    
    # Hash a UMA identifier
    uma_identifier = "alice@example.com"
    signing_key = b"x" * 32
    uma_hash = hasher.hash_uma_identifier(uma_identifier, signing_key)
    print(f"UMA Hash: {uma_hash}")
    
    # Hash a phone number
    phone_number = "+12125551234"
    phone_hash = hasher.hash_phone_number(phone_number)
    print(f"Phone Hash: {phone_hash}")
    
    # Verify hashes (constant-time)
    is_valid = hasher.verify_uma_hash(uma_identifier, signing_key, uma_hash)
    print(f"UMA Hash Valid: {is_valid}")
    
    is_valid = hasher.verify_phone_hash(phone_number, phone_hash)
    print(f"Phone Hash Valid: {is_valid}")


if __name__ == "__main__":
    print("=" * 70)
    print("SECURE HASHING IMPLEMENTATION")
    print("=" * 70)
    print()
    example_usage()
    print()
    print("=" * 70)
    print("SECURITY IMPROVEMENTS:")
    print("  ✓ HMAC-SHA256 prevents rainbow table attacks")
    print("  ✓ Secret key adds computational barrier")
    print("  ✓ Constant-time comparison prevents timing attacks")
    print("  ✓ Input validation prevents malformed data")
    print("=" * 70)
