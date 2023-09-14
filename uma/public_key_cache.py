# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Optional

from uma.protocol import PubkeyResponse


class IPublicKeyCache(ABC):
    @abstractmethod
    def fetch_public_key_for_vasp(self, vasp_domain: str) -> Optional[PubkeyResponse]:
        pass

    @abstractmethod
    def add_public_key_for_vasp(
        self, vasp_domain: str, public_key: PubkeyResponse
    ) -> None:
        pass

    @abstractmethod
    def remove_public_key_for_vasp(self, vasp_domain: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class InMemoryPublicKeyCache(IPublicKeyCache):
    def __init__(self) -> None:
        self._cache: Dict[str, PubkeyResponse] = {}

    def fetch_public_key_for_vasp(self, vasp_domain: str) -> Optional[PubkeyResponse]:
        public_key = self._cache.get(vasp_domain, None)
        if not public_key:
            return None

        return (
            public_key
            if (
                not public_key.expiration_timestamp
                or public_key.expiration_timestamp > datetime.now(timezone.utc)
            )
            else None
        )

    def add_public_key_for_vasp(
        self, vasp_domain: str, public_key: PubkeyResponse
    ) -> None:
        self._cache[vasp_domain] = public_key

    def remove_public_key_for_vasp(self, vasp_domain: str) -> None:
        if vasp_domain in self._cache:
            self._cache.pop(vasp_domain)

    def clear(self) -> None:
        self._cache.clear()
