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

CREATE_UMA_INVITATION_WITH_PAYMENT_MUTATION = f"""
mutation CreateUmaInvitationWithPayment(
    $inviter_uma: String!
    $payment_amount: Float!
    $payment_currency_code: String!
    $payment_currency_symbol: String!
    $payment_currency_name: String!
    $payment_currency_decimals: Int!
    $expires_at: DateTime!
) {{
    create_uma_invitation_with_payment(input: {{
        inviter_uma: $inviter_uma
        payment_amount: $payment_amount
        payment_currency: {{
          code: $payment_currency_code
          symbol: $payment_currency_symbol
          name: $payment_currency_name
          decimals: $payment_currency_decimals
        }}
        expires_at: $expires_at
    }}) {{
        invitation {{
            ...UmaInvitationFragment
        }}
    }}
}}

{INVITATION_FRAGMENT}
"""
