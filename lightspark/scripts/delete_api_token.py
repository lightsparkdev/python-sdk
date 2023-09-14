# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

DELETE_API_TOKEN_MUTATION = """
mutation DeleteApiToken(
    $api_token_id: ID!
) {
    delete_api_token(input: {
        api_token_id: $api_token_id
    }) {
        __typename
    }
}
"""
