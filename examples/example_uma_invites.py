# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import logging
import os

import lightspark

logger = logging.getLogger("uma_invites")
logger.setLevel(logging.DEBUG)

#################################################################
## MODIFY THOSE VARIABLES BEFORE RUNNING THE EXAMPLE
#################################################################
##
## We defined those variables as environment variables, but if you are just
## running the example locally, feel free to just set the values in Python.
##

api_token_id = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_ID")
api_token_secret = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_SECRET")
base_url = os.environ.get("LIGHTSPARK_API_ENDPOINT")
vasp_domain = os.environ.get("LIGHTSPARK_UMA_VASP_DOMAIN")

# Let's start by creating a client

assert api_token_secret
assert api_token_id

client = lightspark.LightsparkSyncClient(
    api_token_client_id=api_token_id,
    api_token_client_secret=api_token_secret,
    base_url=base_url,
)

# Create an invitation
invitation = client.create_uma_invitation_with_incentives(
    inviter_uma=f"$alice@{vasp_domain}",
    inviter_phone_number_e164="+11234567890",
    inviter_region=lightspark.RegionCode.US,
)

print(
    f"Created an invitation with code={invitation.code}, url={invitation.url}, and incentives status={invitation.incentives_status.name}"
)


# Claim an invitation

client.claim_uma_invitation_with_incentives(
    invitation_code=invitation.code,
    invitee_uma=f"$bob@{vasp_domain}",
    invitee_phone_number_e164="+520987654321",
    invitee_region=lightspark.RegionCode.MX,
)

print("Claimed invitation!")


# Claiming an invitation again!

try:
    print("Claiming the same invitation again...")
    client.claim_uma_invitation_with_incentives(
        invitation_code=invitation.code,
        invitee_uma=f"$bob@{vasp_domain}",
        invitee_phone_number_e164="+520987654321",
        invitee_region=lightspark.RegionCode.MX,
    )
    failed = False
except:
    failed = True

assert failed, "Claiming an invitation twice should fail."
print("Claiming an invitation twice failed, as expected!")
