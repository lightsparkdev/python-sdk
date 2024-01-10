# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from typing import Callable, Mapping, Optional, Type, TypeVar

from lightspark.objects.Account import FRAGMENT as AccountFragment
from lightspark.objects.Account import Account
from lightspark.objects.Account import from_json as Account_from_json
from lightspark.objects.ApiToken import FRAGMENT as ApiTokenFragment
from lightspark.objects.ApiToken import ApiToken
from lightspark.objects.ApiToken import from_json as ApiToken_from_json
from lightspark.objects.Channel import FRAGMENT as ChannelFragment
from lightspark.objects.Channel import Channel
from lightspark.objects.Channel import from_json as Channel_from_json
from lightspark.objects.ChannelClosingTransaction import (
    FRAGMENT as ChannelClosingTransactionFragment,
)
from lightspark.objects.ChannelClosingTransaction import ChannelClosingTransaction
from lightspark.objects.ChannelClosingTransaction import (
    from_json as ChannelClosingTransaction_from_json,
)
from lightspark.objects.ChannelOpeningTransaction import (
    FRAGMENT as ChannelOpeningTransactionFragment,
)
from lightspark.objects.ChannelOpeningTransaction import ChannelOpeningTransaction
from lightspark.objects.ChannelOpeningTransaction import (
    from_json as ChannelOpeningTransaction_from_json,
)
from lightspark.objects.ChannelSnapshot import FRAGMENT as ChannelSnapshotFragment
from lightspark.objects.ChannelSnapshot import ChannelSnapshot
from lightspark.objects.ChannelSnapshot import from_json as ChannelSnapshot_from_json
from lightspark.objects.Deposit import FRAGMENT as DepositFragment
from lightspark.objects.Deposit import Deposit
from lightspark.objects.Deposit import from_json as Deposit_from_json
from lightspark.objects.Entity import FRAGMENT as EntityFragment
from lightspark.objects.Entity import Entity
from lightspark.objects.GraphNode import FRAGMENT as GraphNodeFragment
from lightspark.objects.GraphNode import GraphNode
from lightspark.objects.GraphNode import from_json as GraphNode_from_json
from lightspark.objects.Hop import FRAGMENT as HopFragment
from lightspark.objects.Hop import Hop
from lightspark.objects.Hop import from_json as Hop_from_json
from lightspark.objects.IncomingPayment import FRAGMENT as IncomingPaymentFragment
from lightspark.objects.IncomingPayment import IncomingPayment
from lightspark.objects.IncomingPayment import from_json as IncomingPayment_from_json
from lightspark.objects.IncomingPaymentAttempt import (
    FRAGMENT as IncomingPaymentAttemptFragment,
)
from lightspark.objects.IncomingPaymentAttempt import IncomingPaymentAttempt
from lightspark.objects.IncomingPaymentAttempt import (
    from_json as IncomingPaymentAttempt_from_json,
)
from lightspark.objects.Invoice import FRAGMENT as InvoiceFragment
from lightspark.objects.Invoice import Invoice
from lightspark.objects.Invoice import from_json as Invoice_from_json
from lightspark.objects.LightningTransaction import (
    FRAGMENT as LightningTransactionFragment,
)
from lightspark.objects.LightningTransaction import LightningTransaction
from lightspark.objects.LightningTransaction import (
    from_json as LightningTransaction_from_json,
)
from lightspark.objects.LightsparkNode import FRAGMENT as LightsparkNodeFragment
from lightspark.objects.LightsparkNode import LightsparkNode
from lightspark.objects.LightsparkNode import from_json as LightsparkNode_from_json
from lightspark.objects.LightsparkNodeOwner import (
    FRAGMENT as LightsparkNodeOwnerFragment,
)
from lightspark.objects.LightsparkNodeOwner import LightsparkNodeOwner
from lightspark.objects.LightsparkNodeOwner import (
    from_json as LightsparkNodeOwner_from_json,
)
from lightspark.objects.LightsparkNodeWithOSK import (
    FRAGMENT as LightsparkNodeWithOSKFragment,
)
from lightspark.objects.LightsparkNodeWithOSK import LightsparkNodeWithOSK
from lightspark.objects.LightsparkNodeWithOSK import (
    from_json as LightsparkNodeWithOSK_from_json,
)
from lightspark.objects.LightsparkNodeWithRemoteSigning import (
    FRAGMENT as LightsparkNodeWithRemoteSigningFragment,
)
from lightspark.objects.LightsparkNodeWithRemoteSigning import (
    LightsparkNodeWithRemoteSigning,
)
from lightspark.objects.LightsparkNodeWithRemoteSigning import (
    from_json as LightsparkNodeWithRemoteSigning_from_json,
)
from lightspark.objects.Node import FRAGMENT as NodeFragment
from lightspark.objects.Node import Node
from lightspark.objects.Node import from_json as Node_from_json
from lightspark.objects.OnChainTransaction import FRAGMENT as OnChainTransactionFragment
from lightspark.objects.OnChainTransaction import OnChainTransaction
from lightspark.objects.OnChainTransaction import (
    from_json as OnChainTransaction_from_json,
)
from lightspark.objects.OutgoingPayment import FRAGMENT as OutgoingPaymentFragment
from lightspark.objects.OutgoingPayment import OutgoingPayment
from lightspark.objects.OutgoingPayment import from_json as OutgoingPayment_from_json
from lightspark.objects.OutgoingPaymentAttempt import (
    FRAGMENT as OutgoingPaymentAttemptFragment,
)
from lightspark.objects.OutgoingPaymentAttempt import OutgoingPaymentAttempt
from lightspark.objects.OutgoingPaymentAttempt import (
    from_json as OutgoingPaymentAttempt_from_json,
)
from lightspark.objects.PaymentRequest import FRAGMENT as PaymentRequestFragment
from lightspark.objects.PaymentRequest import PaymentRequest
from lightspark.objects.PaymentRequest import from_json as PaymentRequest_from_json
from lightspark.objects.RoutingTransaction import FRAGMENT as RoutingTransactionFragment
from lightspark.objects.RoutingTransaction import RoutingTransaction
from lightspark.objects.RoutingTransaction import (
    from_json as RoutingTransaction_from_json,
)
from lightspark.objects.Signable import FRAGMENT as SignableFragment
from lightspark.objects.Signable import Signable
from lightspark.objects.Signable import from_json as Signable_from_json
from lightspark.objects.SignablePayload import FRAGMENT as SignablePayloadFragment
from lightspark.objects.SignablePayload import SignablePayload
from lightspark.objects.SignablePayload import from_json as SignablePayload_from_json
from lightspark.objects.Transaction import FRAGMENT as TransactionFragment
from lightspark.objects.Transaction import Transaction
from lightspark.objects.Transaction import from_json as Transaction_from_json
from lightspark.objects.UmaInvitation import FRAGMENT as UmaInvitationFragment
from lightspark.objects.UmaInvitation import UmaInvitation
from lightspark.objects.UmaInvitation import from_json as UmaInvitation_from_json
from lightspark.objects.Wallet import FRAGMENT as WalletFragment
from lightspark.objects.Wallet import Wallet
from lightspark.objects.Wallet import from_json as Wallet_from_json
from lightspark.objects.Withdrawal import FRAGMENT as WithdrawalFragment
from lightspark.objects.Withdrawal import Withdrawal
from lightspark.objects.Withdrawal import from_json as Withdrawal_from_json
from lightspark.objects.WithdrawalRequest import FRAGMENT as WithdrawalRequestFragment
from lightspark.objects.WithdrawalRequest import WithdrawalRequest
from lightspark.objects.WithdrawalRequest import (
    from_json as WithdrawalRequest_from_json,
)
from lightspark.requests.requester import Requester

ENTITY = TypeVar("ENTITY", bound=Entity)

ALL_QUERIES: Mapping[Type, str] = {
    Account: """        ... on Account {
            ...AccountFragment
        }
""",
    ApiToken: """        ... on ApiToken {
            ...ApiTokenFragment
        }
""",
    Channel: """        ... on Channel {
            ...ChannelFragment
        }
""",
    ChannelClosingTransaction: """        ... on ChannelClosingTransaction {
            ...ChannelClosingTransactionFragment
        }
""",
    ChannelOpeningTransaction: """        ... on ChannelOpeningTransaction {
            ...ChannelOpeningTransactionFragment
        }
""",
    ChannelSnapshot: """        ... on ChannelSnapshot {
            ...ChannelSnapshotFragment
        }
""",
    Deposit: """        ... on Deposit {
            ...DepositFragment
        }
""",
    Entity: """        ... on Entity {
            ...EntityFragment
        }
""",
    GraphNode: """        ... on GraphNode {
            ...GraphNodeFragment
        }
""",
    Hop: """        ... on Hop {
            ...HopFragment
        }
""",
    IncomingPayment: """        ... on IncomingPayment {
            ...IncomingPaymentFragment
        }
""",
    IncomingPaymentAttempt: """        ... on IncomingPaymentAttempt {
            ...IncomingPaymentAttemptFragment
        }
""",
    Invoice: """        ... on Invoice {
            ...InvoiceFragment
        }
""",
    LightningTransaction: """        ... on LightningTransaction {
            ...LightningTransactionFragment
        }
""",
    LightsparkNode: """        ... on LightsparkNode {
            ...LightsparkNodeFragment
        }
""",
    LightsparkNodeOwner: """        ... on LightsparkNodeOwner {
            ...LightsparkNodeOwnerFragment
        }
""",
    LightsparkNodeWithOSK: """        ... on LightsparkNodeWithOSK {
            ...LightsparkNodeWithOSKFragment
        }
""",
    LightsparkNodeWithRemoteSigning: """        ... on LightsparkNodeWithRemoteSigning {
            ...LightsparkNodeWithRemoteSigningFragment
        }
""",
    Node: """        ... on Node {
            ...NodeFragment
        }
""",
    OnChainTransaction: """        ... on OnChainTransaction {
            ...OnChainTransactionFragment
        }
""",
    OutgoingPayment: """        ... on OutgoingPayment {
            ...OutgoingPaymentFragment
        }
""",
    OutgoingPaymentAttempt: """        ... on OutgoingPaymentAttempt {
            ...OutgoingPaymentAttemptFragment
        }
""",
    PaymentRequest: """        ... on PaymentRequest {
            ...PaymentRequestFragment
        }
""",
    RoutingTransaction: """        ... on RoutingTransaction {
            ...RoutingTransactionFragment
        }
""",
    Signable: """        ... on Signable {
            ...SignableFragment
        }
""",
    SignablePayload: """        ... on SignablePayload {
            ...SignablePayloadFragment
        }
""",
    Transaction: """        ... on Transaction {
            ...TransactionFragment
        }
""",
    UmaInvitation: """        ... on UmaInvitation {
            ...UmaInvitationFragment
        }
""",
    Wallet: """        ... on Wallet {
            ...WalletFragment
        }
""",
    Withdrawal: """        ... on Withdrawal {
            ...WithdrawalFragment
        }
""",
    WithdrawalRequest: """        ... on WithdrawalRequest {
            ...WithdrawalRequestFragment
        }
""",
}
ALL_FRAGMENTS: Mapping[Type, str] = {
    Account: AccountFragment,
    ApiToken: ApiTokenFragment,
    Channel: ChannelFragment,
    ChannelClosingTransaction: ChannelClosingTransactionFragment,
    ChannelOpeningTransaction: ChannelOpeningTransactionFragment,
    ChannelSnapshot: ChannelSnapshotFragment,
    Deposit: DepositFragment,
    Entity: EntityFragment,
    GraphNode: GraphNodeFragment,
    Hop: HopFragment,
    IncomingPayment: IncomingPaymentFragment,
    IncomingPaymentAttempt: IncomingPaymentAttemptFragment,
    Invoice: InvoiceFragment,
    LightningTransaction: LightningTransactionFragment,
    LightsparkNode: LightsparkNodeFragment,
    LightsparkNodeOwner: LightsparkNodeOwnerFragment,
    LightsparkNodeWithOSK: LightsparkNodeWithOSKFragment,
    LightsparkNodeWithRemoteSigning: LightsparkNodeWithRemoteSigningFragment,
    Node: NodeFragment,
    OnChainTransaction: OnChainTransactionFragment,
    OutgoingPayment: OutgoingPaymentFragment,
    OutgoingPaymentAttempt: OutgoingPaymentAttemptFragment,
    PaymentRequest: PaymentRequestFragment,
    RoutingTransaction: RoutingTransactionFragment,
    Signable: SignableFragment,
    SignablePayload: SignablePayloadFragment,
    Transaction: TransactionFragment,
    UmaInvitation: UmaInvitationFragment,
    Wallet: WalletFragment,
    Withdrawal: WithdrawalFragment,
    WithdrawalRequest: WithdrawalRequestFragment,
}
ALL_JSON_LOADERS: Mapping[Type, Callable] = {
    Account: Account_from_json,
    ApiToken: ApiToken_from_json,
    Channel: Channel_from_json,
    ChannelClosingTransaction: ChannelClosingTransaction_from_json,
    ChannelOpeningTransaction: ChannelOpeningTransaction_from_json,
    ChannelSnapshot: ChannelSnapshot_from_json,
    Deposit: Deposit_from_json,
    GraphNode: GraphNode_from_json,
    Hop: Hop_from_json,
    IncomingPayment: IncomingPayment_from_json,
    IncomingPaymentAttempt: IncomingPaymentAttempt_from_json,
    Invoice: Invoice_from_json,
    LightningTransaction: LightningTransaction_from_json,
    LightsparkNode: LightsparkNode_from_json,
    LightsparkNodeOwner: LightsparkNodeOwner_from_json,
    LightsparkNodeWithOSK: LightsparkNodeWithOSK_from_json,
    LightsparkNodeWithRemoteSigning: LightsparkNodeWithRemoteSigning_from_json,
    Node: Node_from_json,
    OnChainTransaction: OnChainTransaction_from_json,
    OutgoingPayment: OutgoingPayment_from_json,
    OutgoingPaymentAttempt: OutgoingPaymentAttempt_from_json,
    PaymentRequest: PaymentRequest_from_json,
    RoutingTransaction: RoutingTransaction_from_json,
    Signable: Signable_from_json,
    SignablePayload: SignablePayload_from_json,
    Transaction: Transaction_from_json,
    UmaInvitation: UmaInvitation_from_json,
    Wallet: Wallet_from_json,
    Withdrawal: Withdrawal_from_json,
    WithdrawalRequest: WithdrawalRequest_from_json,
}


def get_entity(
    requester: Requester, entity_id: str, entity_class: Type[ENTITY]
) -> Optional[ENTITY]:
    json = requester.execute_graphql(
        f"""
query GetEntity($id: ID!) {{
    entity(id: $id) {{
{ALL_QUERIES[entity_class]}
    }}
}}

{ALL_FRAGMENTS[entity_class]}
""",
        {"id": entity_id},
    )
    if not json["entity"]:
        return None
    return ALL_JSON_LOADERS[entity_class](requester, json["entity"])
