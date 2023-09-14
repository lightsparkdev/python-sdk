# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from uma.version import (
    MAJOR_VERSION,
    MINOR_VERSION,
    UMA_PROTOCOL_VERSION,
    ParsedVersion,
    get_highest_supported_version_for_major_version,
    is_version_supported,
    select_highest_supported_version,
    select_lower_version,
)


def select_lower_version() -> None:
    assert select_lower_version("1.1", "1.1") == "1.1"
    assert select_lower_version("1.2", "1.1") == "1.1"
    assert select_lower_version("1.1", "1.2") == "1.1"
    assert select_lower_version("1.3", "2.1") == "1.3"
    assert select_lower_version("2.1", "1.3") == "1.3"


def test_get_highest_version() -> None:
    assert (
        get_highest_supported_version_for_major_version(major_version=MAJOR_VERSION + 1)
        is None
    )
    assert get_highest_supported_version_for_major_version(
        major_version=MAJOR_VERSION
    ) == ParsedVersion.load(UMA_PROTOCOL_VERSION)


def test_is_version_supported() -> None:
    assert not is_version_supported(f"{MAJOR_VERSION + 1}.0")
    assert is_version_supported(UMA_PROTOCOL_VERSION)
    assert is_version_supported(f"{MAJOR_VERSION}.{MINOR_VERSION-1}")
    assert is_version_supported(f"{MAJOR_VERSION}.{MINOR_VERSION+1}")


def test_selected_highest_version() -> None:
    assert (
        select_highest_supported_version(
            [MAJOR_VERSION - 1, MAJOR_VERSION, MAJOR_VERSION + 1]
        )
        == UMA_PROTOCOL_VERSION
    )
