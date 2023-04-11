# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
import logging
import re
import secrets
from datetime import datetime, timedelta, timezone
from platform import python_version, release, system
from typing import Any, Mapping, Optional
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth
from requests.utils import default_user_agent

from lightspark.exceptions import LightsparkException
from lightspark.requests.encoder import Encoder
from lightspark.utils.crypto import sign_payload
from lightspark.version import __version__

DEFAULT_BASE_URL = "https://api.lightspark.com/graphql/2023-04-04"

logger = logging.getLogger("lightspark")


class Requester:
    def __init__(
        self,
        api_token_client_id: str,
        api_token_client_secret: str,
        base_url: Optional[str] = None,
        http_host: Optional[str] = None,
    ) -> None:
        self.base_url = base_url or DEFAULT_BASE_URL
        self.graphql_session = requests.Session()
        self.graphql_session.auth = HTTPBasicAuth(
            api_token_client_id, api_token_client_secret
        )

        if http_host:
            self.graphql_session.mount("https://", HTTPSAdapter(http_host))
            self.graphql_session.headers.update({"Host": http_host})

    def execute_graphql(
        self,
        query: str,
        variables: Optional[Mapping[str, Any]],
        signing_key: Optional[bytes] = None,
    ) -> Mapping[str, Any]:
        operation = re.match(r"\s*(?:query|mutation)\s+(\w+)", query, re.IGNORECASE)
        payload = json.dumps(
            {
                "operationName": operation.group(1) if operation else None,
                "query": query,
                "variables": variables or {},
                "nonce": secrets.randbits(32) if signing_key else None,
                "expires_at": (datetime.utcnow() + timedelta(hours=1))
                .replace(tzinfo=timezone.utc)
                .isoformat()
                if signing_key
                else None,
            },
            cls=Encoder,
        ).encode("utf8")

        signing = sign_payload(payload, signing_key) if signing_key else None

        user_agent = self.user_agent_string()
        logger.debug(
            "Sending request to GraphQL with query = %s, payload = %s}", query, payload
        )
        r = self.graphql_session.post(
            url=self.base_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-GraphQL-Operation": operation.group(1) if operation else None,
                "X-Lightspark-Signing": signing,
                "User-Agent": user_agent + f" {default_user_agent()}",
                "X-Lightspark-SDK": user_agent,
            },
        )
        try:
            r.raise_for_status()
            result = r.json()
            if "errors" in result:
                errors = result["errors"]
                raise LightsparkException(
                    "GRAPHQL_ERROR", f"A GraphQL error occurred: {errors}"
                )  # TODO better error handling
            return result["data"]
        except requests.HTTPError as e:
            logger.error("HTTP request error. Status code: %d", r.status_code)
            raise LightsparkException("HTTP_ERROR", str(e)) from e
        except Exception as e:
            logger.exception(e)

            try:
                logger.error(r.text)
            # TODO pylint is right here... let's make it better.
            except Exception:  # pylint: disable=broad-except
                pass
            raise e

    def user_agent_string(self):
        # Will produce something like: 	lightspark-python-sdk/0.5.1 python/3.11.2 Darwin/22.1.0
        return f"lightspark-python-sdk/{__version__} python/{python_version()} {system()}/{release()}"


class HTTPSAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, server_hostname: str, *args, **kwargs):
        self.server_hostname = server_hostname
        super().__init__(*args, **kwargs)

    def get_connection(self, url, proxies=None):
        url = urlparse(url).geturl()
        return self.poolmanager.connection_from_url(
            url, pool_kwargs={"server_hostname": self.server_hostname}
        )
