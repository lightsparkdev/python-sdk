# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from abc import ABC, abstractmethod
from typing import Optional

import lightspark


class IUmaInvoiceCreator(ABC):
    @abstractmethod
    def create_uma_invoice(
        self,
        amount_msats: int,
        metadata: str,
    ) -> str:
        pass


class LightsparkUmaInvoiceCreator(IUmaInvoiceCreator):
    def __init__(
        self,
        lightspark_client: lightspark.LightsparkSyncClient,
        node_id: str,
        expiry_secs: Optional[int],
    ) -> None:
        self.lightspark_client = lightspark_client
        self.node_id = node_id
        self.expiry_secs = expiry_secs

    def create_uma_invoice(
        self,
        amount_msats: int,
        metadata: str,
    ) -> str:
        invoice = self.lightspark_client.create_uma_invoice(
            self.node_id,
            amount_msats=amount_msats,
            metadata=metadata,
            expiry_secs=self.expiry_secs,
        )
        return invoice.data.encoded_payment_request
