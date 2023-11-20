# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.UmaInvitation import FRAGMENT as INVITATION_FRAGMENT

CREATE_UMA_INVITATION_MUTATION = f"""
mutation CreateUmaInvitation(
    $inviter_uma: String!
) {{
    create_uma_invitation(input: {{
        inviter_uma: $inviter_uma
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""

CREATE_UMA_INVITATION_WITH_INCENTIVES_MUTATION = f"""
mutation CreateUmaInvitationWithIncentives(
    $inviter_uma: String!
    $inviter_phone_hash: String!
    $inviter_region: RegionCode!
) {{
    create_uma_invitation_with_incentives(input: {{
        inviter_uma: $inviter_uma
        inviter_phone_hash: $inviter_phone_hash
        inviter_region: $inviter_region
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""
