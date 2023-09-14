# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.Account import FRAGMENT as AccountFragment

CURRENT_ACCOUNT_QUERY = f"""
query GetCurrentAccount {{
    current_account {{
        ...AccountFragment
    }}
}}

{AccountFragment}
"""
