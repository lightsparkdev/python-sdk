# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime

from lightspark.objects.WebhookEventType import WebhookEventType

SIGNATURE_HEADER = "lightspark-signature"


@dataclass
class WebhookEvent:
    event_type: WebhookEventType
    event_id: str
    timestamp: datetime
    entity_id: str

    @classmethod
    def verify_and_parse(
        cls, data: bytes, hexdigest: str, webhook_secret: str
    ) -> "WebhookEvent":
        """Verifies the signature and parses the message into a
        WebhookEvent object.

        Args:
          data: the POST message body received by the webhook.
          hexdigest: the message signature sent in the
            `lightspark-signature` header.
          webhook_secret: the webhook secret configured at the
            Lightspark API configuration.

        Returns:
          A parsed WebhookEvent object.

        Raises:
          A ValueError if the message signature is invalid.
        """
        if not isinstance(data, bytes):
            raise TypeError(f"'data' should be bytes, got {type(data)}")

        sig = hmac.new(
            webhook_secret.encode("ascii"), msg=data, digestmod=hashlib.sha256
        )
        if sig.hexdigest().lower() != hexdigest.lower():
            raise ValueError("Webhook message hash does not match signature")

        return cls.parse(data)

    @classmethod
    def parse(cls, data: bytes) -> "WebhookEvent":
        """Parses the message into a WebhookEvent object.

        Args:
          data: the POST message body received by the webhook.

        Returns:
          A parsed WebhookEvent object.

        Raises:
          A ValueError if the event type is unrecognized.
        """
        if not isinstance(data, bytes):
            raise TypeError(f"'data' should be bytes, got {type(data)}")

        event = json.loads(data.decode("utf-8"))
        return cls(
            event_type=WebhookEventType[event["event_type"]],
            event_id=event["event_id"],
            timestamp=datetime.fromisoformat(event["timestamp"]),
            entity_id=event["entity_id"],
        )
