# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.UmaInvitation import FRAGMENT as INVITATION_FRAGMENT

CANCEL_UMA_INVITATION_MUTATION = f"""
mutation CancelUmaInvitation(
    $invite_code: String!
) {{
    cancel_uma_invitation(input: {{
        invite_code: $invite_code
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""
