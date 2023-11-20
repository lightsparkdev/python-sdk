# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from lightspark.objects.UmaInvitation import FRAGMENT as INVITATION_FRAGMENT

CLAIM_UMA_INVITATION_MUTATION = f"""
mutation ClaimUmaInvitation(
    $invitation_code: String!
    $invitee_uma: String!
) {{
    claim_uma_invitation(input: {{
        invitation_code: $invitation_code
        invitee_uma: $invitee_uma
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""


CLAIM_UMA_INVITATION_WITH_INCENTIVES_MUTATION = f"""
mutation ClaimUmaInvitationWithIncentives(
    $invitation_code: String!
    $invitee_uma: String!
    $invitee_phone_hash: String!
    $invitee_region: RegionCode!
) {{
    claim_uma_invitation_with_incentives(input: {{
        invitation_code: $invitation_code
        invitee_uma: $invitee_uma
        invitee_phone_hash: $invitee_phone_hash
        invitee_region: $invitee_region
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""
