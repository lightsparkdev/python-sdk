#!/usr/bin/env python3
"""
FIXED VERSION: Secure Webhook Parsing with Input Validation

This module contains the fixed webhook parsing implementation that addresses:
- Missing field validation
- Type validation
- DoS via large payloads
- Information disclosure via error messages

Changes:
- Comprehensive input validation
- Schema validation
- Sanitized error messages
- Size limits on payloads
"""

import json
import hmac
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, Dict
from enum import Enum


class WebhookEventType(Enum):
    """Supported webhook event types"""
    PAYMENT_FINISHED = "PAYMENT_FINISHED"
    NODE_STATUS = "NODE_STATUS"
    INVOICE_CREATED = "INVOICE_CREATED"
    WITHDRAWAL_COMPLETED = "WITHDRAWAL_COMPLETED"


class WebhookValidationError(Exception):
    """Custom exception for webhook validation errors"""
    pass


@dataclass
class WebhookEvent:
    """Secure webhook event with validation"""
    event_type: WebhookEventType
    event_id: str
    timestamp: datetime
    entity_id: str
    wallet_id: Optional[str] = None
    
    # Configuration constants
    MAX_PAYLOAD_SIZE = 1024 * 1024  # 1MB max payload
    MAX_STRING_LENGTH = 1000  # Max length for string fields
    
    @classmethod
    def verify_and_parse(
        cls, 
        data: bytes, 
        hex_digest: str, 
        webhook_secret: str
    ) -> "WebhookEvent":
        """
        Verifies the signature and parses the message into a WebhookEvent object.
        
        Args:
            data: The POST message body received by the webhook
            hex_digest: The message signature sent in the header
            webhook_secret: The webhook secret configured in the API
        
        Returns:
            A parsed WebhookEvent object
        
        Raises:
            WebhookValidationError: If validation fails
            ValueError: If signature is invalid
        """
        # Type validation
        if not isinstance(data, bytes):
            raise TypeError(f"'data' should be bytes, got {type(data)}")
        
        # Size validation (prevent DoS)
        if len(data) > cls.MAX_PAYLOAD_SIZE:
            raise WebhookValidationError(
                f"Payload too large: {len(data)} bytes (max: {cls.MAX_PAYLOAD_SIZE})"
            )
        
        # Verify HMAC signature (constant-time comparison)
        mac = hmac.new(
            webhook_secret.encode("ascii"), 
            msg=data, 
            digestmod="sha256"
        )
        
        try:
            expected_digest = bytes.fromhex(hex_digest)
        except ValueError:
            raise ValueError("Invalid signature format: must be hex-encoded")
        
        if not hmac.compare_digest(mac.digest(), expected_digest):
            raise ValueError("Webhook message hash does not match signature")
        
        # Parse with validation
        return cls.parse(data)
    
    @classmethod
    def parse(cls, data: bytes) -> "WebhookEvent":
        """
        Parses the message into a WebhookEvent object with comprehensive validation.
        
        Args:
            data: The POST message body received by the webhook
        
        Returns:
            A parsed WebhookEvent object
        
        Raises:
            WebhookValidationError: If validation fails
        """
        # Type validation
        if not isinstance(data, bytes):
            raise TypeError(f"'data' should be bytes, got {type(data)}")
        
        # Size validation
        if len(data) > cls.MAX_PAYLOAD_SIZE:
            raise WebhookValidationError(
                f"Payload too large: {len(data)} bytes"
            )
        
        # Parse JSON with error handling
        try:
            event = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as e:
            # Sanitized error message (don't expose payload content)
            raise WebhookValidationError(
                f"Invalid JSON format at position {e.pos}"
            ) from e
        except UnicodeDecodeError as e:
            raise WebhookValidationError(
                "Invalid UTF-8 encoding in payload"
            ) from e
        
        # Validate that event is a dictionary
        if not isinstance(event, dict):
            raise WebhookValidationError(
                f"Webhook payload must be a JSON object, got {type(event).__name__}"
            )
        
        # Validate required fields exist
        required_fields = ["event_type", "event_id", "timestamp", "entity_id"]
        missing_fields = [field for field in required_fields if field not in event]
        
        if missing_fields:
            raise WebhookValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate and parse event_type
        try:
            event_type_str = cls._validate_string(
                event.get("event_type"), 
                "event_type",
                max_length=100
            )
            event_type = WebhookEventType(event_type_str)
        except ValueError as e:
            # Don't expose all valid types in error message
            raise WebhookValidationError(
                "Invalid event_type value"
            ) from e
        
        # Validate and parse event_id
        event_id = cls._validate_string(
            event.get("event_id"), 
            "event_id",
            max_length=cls.MAX_STRING_LENGTH
        )
        
        # Validate and parse timestamp
        timestamp_str = cls._validate_string(
            event.get("timestamp"),
            "timestamp",
            max_length=100
        )
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError as e:
            raise WebhookValidationError(
                "Invalid timestamp format (expected ISO 8601)"
            ) from e
        
        # Validate and parse entity_id
        entity_id = cls._validate_string(
            event.get("entity_id"),
            "entity_id",
            max_length=cls.MAX_STRING_LENGTH
        )
        
        # Validate optional wallet_id
        wallet_id = None
        if "wallet_id" in event and event["wallet_id"] is not None:
            wallet_id = cls._validate_string(
                event["wallet_id"],
                "wallet_id",
                max_length=cls.MAX_STRING_LENGTH
            )
        
        # Create and return validated event
        return cls(
            event_type=event_type,
            event_id=event_id,
            timestamp=timestamp,
            entity_id=entity_id,
            wallet_id=wallet_id
        )
    
    @staticmethod
    def _validate_string(
        value: Any, 
        field_name: str, 
        max_length: int = MAX_STRING_LENGTH
    ) -> str:
        """
        Validate that a value is a string with appropriate length.
        
        Args:
            value: The value to validate
            field_name: Name of the field (for error messages)
            max_length: Maximum allowed length
        
        Returns:
            The validated string
        
        Raises:
            WebhookValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise WebhookValidationError(
                f"Field '{field_name}' must be a string, got {type(value).__name__}"
            )
        
        if len(value) == 0:
            raise WebhookValidationError(
                f"Field '{field_name}' cannot be empty"
            )
        
        if len(value) > max_length:
            raise WebhookValidationError(
                f"Field '{field_name}' exceeds maximum length ({max_length} chars)"
            )
        
        return value


# Example usage
def example_usage():
    """Example of secure webhook parsing"""
    
    # Valid webhook payload
    valid_payload = {
        "event_type": "PAYMENT_FINISHED",
        "event_id": "evt_123456",
        "timestamp": "2026-01-18T13:00:00+00:00",
        "entity_id": "entity_789",
        "wallet_id": "wallet_abc"
    }
    
    data = json.dumps(valid_payload).encode('utf-8')
    
    # Create HMAC signature
    webhook_secret = "my_webhook_secret"
    mac = hmac.new(
        webhook_secret.encode("ascii"),
        msg=data,
        digestmod="sha256"
    )
    signature = mac.digest().hex()
    
    print("Testing secure webhook parsing...")
    print(f"Payload: {valid_payload}")
    print(f"Signature: {signature[:32]}...")
    print()
    
    try:
        event = WebhookEvent.verify_and_parse(data, signature, webhook_secret)
        print(f"✓ Successfully parsed webhook:")
        print(f"  Event Type: {event.event_type.value}")
        print(f"  Event ID: {event.event_id}")
        print(f"  Timestamp: {event.timestamp}")
        print(f"  Entity ID: {event.entity_id}")
        print(f"  Wallet ID: {event.wallet_id}")
    except (WebhookValidationError, ValueError) as e:
        print(f"✗ Validation failed: {e}")


if __name__ == "__main__":
    print("=" * 70)
    print("SECURE WEBHOOK PARSING")
    print("=" * 70)
    print()
    example_usage()
    print()
    print("=" * 70)
    print("SECURITY IMPROVEMENTS:")
    print("  ✓ Comprehensive field validation")
    print("  ✓ Type checking for all fields")
    print("  ✓ Size limits prevent DoS attacks")
    print("  ✓ Sanitized error messages prevent info disclosure")
    print("  ✓ Constant-time signature verification")
    print("  ✓ Schema validation for event types")
    print("=" * 70)
