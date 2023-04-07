# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved
"""Sample Lightspark Webhooks Flask App.

Install Flask (pip install flask) and then run this like:

  flask --app flask_webhook_server run --port 5001
"""

import lightspark
from flask import Flask, request

app = Flask(__name__)

# Get this from the API Configuration page.
WEBHOOK_SECRET = "CHANGE_ME"


@app.route("/lightspark-webhook", methods=["POST"])
def webhook():
    event = lightspark.WebhookEvent.verify_and_parse(
        request.data, request.headers.get(lightspark.SIGNATURE_HEADER), WEBHOOK_SECRET
    )

    if event.event_type == lightspark.WebhookEventType.NODE_STATUS:
        print(f"Node {event.data.id}'s wallet status is {event.data.wallet_status}.")

    elif event.event_type == lightspark.WebhookEventType.PAYMENT_FINISHED:
        print(
            f"A payment for {event.data.amount.value} {event.data.amount.unit} completed."
        )

    return "OK"
