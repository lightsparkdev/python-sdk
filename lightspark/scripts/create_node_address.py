# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

CREATE_NODE_ADDRESS_MUTATION = """
mutation CreateNodeWalletAddress(
    $node_id: ID!
) {
    create_node_wallet_address(input: {
        node_id: $node_id
    }) {
        wallet_address
    }
}
"""
