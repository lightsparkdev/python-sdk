# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved
"""Sample Lightspark Webhooks Flask App.

Install Flask (pip install flask) and then run this like:

  pipenv run flask --app examples.flask_remote_signin_server run --port 5001
"""

import os
import lightspark
from flask import Flask, request

app = Flask(__name__)

# Get this from the API Configuration page.
webhook_secret = os.environ.get("RK_WEBHOOK_SECRET")

api_token_client_id = os.environ.get("RK_API_CLIENT_ID")
api_token_client_secret = os.environ.get("RK_API_CLIENT_SECRET")

master_seed = os.environ.get("RK_MASTER_SEED_HEX")


@app.route("/ping", methods=["GET"])
def ping():
    print("ping")
    return "OK"


@app.route("/lightspark-webhook", methods=["POST"])
def webhook():
    client = lightspark.LightsparkSyncClient(
        api_token_client_id=api_token_client_id,
        api_token_client_secret=api_token_client_secret,
        base_url=os.environ.get("RK_API_ENDPOINT"),
    )
    validator = lightspark.PositiveValidator()
    handler = lightspark.RemoteSigningWebhookEventHandler(
        client=client, master_seed=bytes.fromhex(master_seed), validator=validator
    )

    handler.handle_remote_signing_webhook_request(
        request.data, request.headers.get(lightspark.SIGNATURE_HEADER), webhook_secret
    )
    return "OK"
