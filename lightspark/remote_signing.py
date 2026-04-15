from typing import Any
from dataclasses import dataclass
import json
import lightspark_crypto as lsc
import lightspark


class PositiveValidator(lsc.Validation):
    @staticmethod
    def should_sign(webhook: Any) -> bool:  # ty:ignore[invalid-method-override]
        return True


@dataclass
class RemoteSigningWebhookEventHandler:
    client: lightspark.LightsparkSyncClient
    master_seed: bytes
    validator: lsc.Validation

    def __init__(
        self,
        client: lightspark.LightsparkSyncClient,
        master_seed: bytes,
        validator: lsc.Validation,
    ):
        self.client = client
        self.master_seed = master_seed
        self.validator = validator

    def handle_remote_signing_webhook_request(
        self, data: bytes, hexdigest: str, webhook_secret: str
    ):
        response = lsc.handle_remote_signing_webhook_event(
            data, hexdigest, webhook_secret, self.master_seed, self.validator
        )
        variables = json.loads(response.variables)
        self.client.execute_graphql_request(response.query, variables)
