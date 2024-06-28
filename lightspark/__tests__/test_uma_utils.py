import datetime
import logging
from unittest.mock import patch
from lightspark import LightsparkSyncClient

logger = logging.getLogger("lightspark")
logger.setLevel(logging.DEBUG)


class TestUmaUtils:
    @patch("lightspark.lightspark_client.datetime")
    def test_hash_uma_identifier_same_month(self, mock_datetime):
        client = LightsparkSyncClient("", "")
        priv_key_bytes = b"xyz"
        mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 0, 0, 0)

        hashed_uma = client.hash_uma_identifier("user@domain.com", priv_key_bytes)
        hashed_uma_same_month = client.hash_uma_identifier(
            "user@domain.com", priv_key_bytes
        )

        logger.debug(hashed_uma)
        assert hashed_uma_same_month == hashed_uma

    @patch("lightspark.lightspark_client.datetime")
    def test_hash_uma_identifier_different_month(self, mock_datetime):
        client = LightsparkSyncClient("", "")
        priv_key_bytes = b"xyz"

        mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 0, 0, 0)
        hashed_uma = client.hash_uma_identifier("user@domain.com", priv_key_bytes)

        mock_datetime.now.return_value = datetime.datetime(2021, 2, 1, 0, 0, 0)
        hashed_uma_diff_month = client.hash_uma_identifier(
            "user@domain.com", priv_key_bytes
        )

        logger.debug(hashed_uma)
        logger.debug(hashed_uma_diff_month)
        assert hashed_uma_diff_month != hashed_uma
