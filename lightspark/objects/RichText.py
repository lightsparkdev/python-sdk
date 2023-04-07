# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester


@dataclass
class RichText:
    requester: Requester

    text: str


FRAGMENT = """
fragment RichTextFragment on RichText {
    __typename
    rich_text_text: text
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> RichText:
    return RichText(
        requester=requester,
        text=obj["rich_text_text"],
    )
