from datetime import datetime

import pytest

import lightspark


class TestWebhooks:
    @pytest.mark.parametrize(
        "hex_digest",
        [
            pytest.param(
                "62a8829aeb48b4142533520b1f7f86cdb1ee7d718bf3ea15bc1c662d4c453b74",
                id="lowercase",
            ),
            pytest.param(
                "62A8829AEB48B4142533520B1F7F86CDB1EE7D718BF3EA15BC1C662D4C453B74",
                id="uppercase",
            ),
        ],
    )
    def test_valid_data_parses(self, hex_digest: str):
        data = b'{"event_type": "NODE_STATUS", "event_id": "1615c8be5aa44e429eba700db2ed8ca5", "timestamp": "2023-05-17T23:56:47.874449+00:00", "entity_id": "lightning_node:01882c25-157a-f96b-0000-362d42b64397"}'
        secret = "3gZ5oQQUASYmqQNuEk0KambNMVkOADDItIJjzUlAWjX"

        webhook = lightspark.WebhookEvent.verify_and_parse(data, hex_digest, secret)

        assert (
            webhook.entity_id == "lightning_node:01882c25-157a-f96b-0000-362d42b64397"
        )
        assert webhook.event_id == "1615c8be5aa44e429eba700db2ed8ca5"
        assert webhook.event_type == lightspark.WebhookEventType.NODE_STATUS
        assert webhook.timestamp == datetime.fromisoformat(
            "2023-05-17T23:56:47.874449+00:00"
        )

    @pytest.mark.parametrize(
        "hex_digest",
        [
            pytest.param("deadbeef", id="wrong length"),
            pytest.param("a" * 64, id="incorrect"),
            pytest.param("NotAHexString", id="not hex"),
            pytest.param(
                "62a8829aeb48b4142533520b1f7f86cdb1ee7d718bf3ea15bc1c662d4c453b74"
                + "qq",
                id="extra bytes",
            ),
        ],
    )
    def test_invalid_data_raises_value_error(self, hex_digest: str):
        data = b'{"event_type": "NODE_STATUS", "event_id": "1615c8be5aa44e429eba700db2ed8ca5", "timestamp": "2023-05-17T23:56:47.874449+00:00", "entity_id": "lightning_node:01882c25-157a-f96b-0000-362d42b64397"}'
        secret = "3gZ5oQQUASYmqQNuEk0KambNMVkOADDItIJjzUlAWjX"

        with pytest.raises(ValueError):
            lightspark.WebhookEvent.verify_and_parse(data, hex_digest, secret)

    def test_invalid_data_type_raises_type_error(self):
        data = 1
        hex_digest = "deadbeef"
        secret = "3gZ5oQQUASYmqQNuEk0KambNMVkOADDItIJjzUlAWjX"

        with pytest.raises(TypeError):
            lightspark.WebhookEvent.verify_and_parse(data, hex_digest, secret)  # type: ignore
