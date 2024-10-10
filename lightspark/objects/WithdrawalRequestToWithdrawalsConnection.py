# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, List, Mapping

from lightspark.requests.requester import Requester

from .Withdrawal import Withdrawal
from .Withdrawal import from_json as Withdrawal_from_json


@dataclass
class WithdrawalRequestToWithdrawalsConnection:
    requester: Requester

    count: int
    """The total count of objects in this connection, using the current filters. It is different from the number of objects returned in the current page (in the `entities` field)."""

    entities: List[Withdrawal]
    """The withdrawals for the current page of this connection."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "withdrawal_request_to_withdrawals_connection_count": self.count,
            "withdrawal_request_to_withdrawals_connection_entities": [
                e.to_json() for e in self.entities
            ],
        }


FRAGMENT = """
fragment WithdrawalRequestToWithdrawalsConnectionFragment on WithdrawalRequestToWithdrawalsConnection {
    __typename
    withdrawal_request_to_withdrawals_connection_count: count
    withdrawal_request_to_withdrawals_connection_entities: entities {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> WithdrawalRequestToWithdrawalsConnection:
    return WithdrawalRequestToWithdrawalsConnection(
        requester=requester,
        count=obj["withdrawal_request_to_withdrawals_connection_count"],
        entities=list(
            map(
                # pylint: disable=unnecessary-lambda
                lambda e: Withdrawal_from_json(requester, e),
                obj["withdrawal_request_to_withdrawals_connection_entities"],
            )
        ),
    )
