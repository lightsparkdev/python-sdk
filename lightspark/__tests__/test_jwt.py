# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from uuid import uuid4

import jwt

from lightspark import LightsparkSyncClient

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MEMwBQYDK2VxAzoA5nZmdwgDoQuVF5sZlx26RdheC0JwXi1PNtnm6EaoffqFBxYO
ksn8HvmMQIeDYL1Tyl/FOpOUIlIA
-----END PUBLIC KEY-----
"""

PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MEcCAQAwBQYDK2VxBDsEOaHk7Bad3cUQvHFZH3W8GHEMLcUnWIl/HD7qgndZnHfe
6ZA+QXYswQmvz+ulvOwRBO1c2S46JKJMJA==
-----END PRIVATE KEY-----
"""


class TestJWT:
    def test_generate_key(self):
        client = LightsparkSyncClient("", "")
        public, private = client.generate_jwt_key()
        assert "BEGIN PUBLIC KEY" in public
        assert "BEGIN PRIVATE KEY" in private

    def test_create_jwt(self):
        client = LightsparkSyncClient("", "")
        user_id = str(uuid4())
        token = client.generate_wallet_jwt(PRIVATE_KEY, user_id)
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["EdDSA"],
            audience="https://api.lightspark.com",
            options={"require": ["exp", "iat", "sub"]},
        )
        assert payload["sub"] == user_id
        assert payload["exp"] > payload["iat"]
