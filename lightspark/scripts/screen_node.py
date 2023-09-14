# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

SCREEN_NODE_MUTATION = """
mutation ScreenNode(
    $provider: ComplianceProvider!
    $node_pubkey: String!
) {
    screen_node(input: {
        provider: $provider
        node_pubkey: $node_pubkey
    }) {
        rating
    }
}
"""
