# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.ApiToken import FRAGMENT as ApiTokenFragment

CREATE_API_TOKEN_MUTATION = f"""
mutation CreateApiToken(
    $name: String!
    $permissions: [Permission!]!
) {{
    create_api_token(input: {{
        name: $name
        permissions: $permissions
    }}) {{
        api_token {{
            ...ApiTokenFragment
        }}
        client_secret
    }}
}}

{ApiTokenFragment}
"""
