# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
from dataclasses import dataclass
from functools import total_ordering
from typing import List, Optional

MAJOR_VERSION = 0
MINOR_VERSION = 1
UMA_PROTOCOL_VERSION = f"{MAJOR_VERSION}.{MINOR_VERSION}"


@total_ordering
@dataclass
class ParsedVersion:
    major: int
    minor: int

    @classmethod
    def load(cls, version: str) -> "ParsedVersion":
        [major, minor] = version.split(".")
        return ParsedVersion(major=int(major), minor=int(minor))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __lt__(self, other: "ParsedVersion") -> bool:
        return self.major < other.major or (
            self.major == other.major and self.minor < other.minor
        )


def get_supported_major_versions() -> List[int]:
    """
    In the future, we may want to support multiple major versions in the same SDK,
    but for now, this keeps things simple.
    """
    return [MAJOR_VERSION]


def get_highest_supported_version_for_major_version(
    major_version: int,
) -> Optional[ParsedVersion]:
    """
    Note that this also only supports a single major version for now. If we support
    more than one major version in the future, we'll need to change this.
    """
    return (
        ParsedVersion.load(UMA_PROTOCOL_VERSION)
        if major_version == MAJOR_VERSION
        else None
    )


def select_highest_supported_version(
    other_vasp_supported_major_versions: List[int],
) -> Optional[str]:
    supported_major_versions = get_supported_major_versions()

    highest_version = None
    for other_vasp_major_version in other_vasp_supported_major_versions:
        if other_vasp_major_version not in supported_major_versions:
            continue

        if not highest_version or other_vasp_major_version > highest_version.major:
            highest_version = get_highest_supported_version_for_major_version(
                other_vasp_major_version
            )

    return str(highest_version) if highest_version else None


def select_lower_version(version_1: str, version_2: str) -> str:
    return (
        version_1
        if ParsedVersion.load(version_1) < ParsedVersion.load(version_2)
        else version_2
    )


def is_version_supported(version: str) -> bool:
    parsed_version = ParsedVersion.load(version)
    return parsed_version.major in get_supported_major_versions()


def get_supported_major_versions_from_error(error_json: str) -> List[int]:
    error = json.loads(error_json)
    return error["supportedMajorVersions"]
