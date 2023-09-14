# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
from typing import List


class UnsupportedVersionException(Exception):
    def __init__(
        self, unsupported_version: str, supported_major_versions: List[int]
    ) -> None:
        super().__init__(f"Version {unsupported_version} not supported.")
        self.unsupported_version = unsupported_version
        self.supported_major_versions = supported_major_versions

    def to_json(self) -> str:
        return json.dumps({"supportedMajorVersions": self.supported_major_versions})


class InvalidRequestException(Exception):
    pass


class InvalidSignatureException(Exception):
    def __init__(self) -> None:
        super().__init__("Cannot verify signature.")
