# Copyright ©, 2026-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark import (
    LightsparkSyncClient,
    PositiveValidator,
    RemoteSigningWebhookEventHandler,
)


class TestRemoteSigning:
    def test_master_seed_not_in_repr(self) -> None:
        client = LightsparkSyncClient("", "")
        handler = RemoteSigningWebhookEventHandler(
            client=client,
            master_seed=b"1234",
            validator=PositiveValidator(),
        )

        assert "1234" not in repr(handler)
