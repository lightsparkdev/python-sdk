# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.UmaInvitation import FRAGMENT as INVITATION_FRAGMENT

FETCH_UMA_INVITATION_QUERY = f"""
query FetchInvitation(
    $invitation_code: String!
) {{
    uma_invitation_by_code(code: $invitation_code) {{
        ...InvitationFragment
    }}
}}

{INVITATION_FRAGMENT}
"""
