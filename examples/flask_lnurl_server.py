import json
import os
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from flask import Flask, abort, request
from flask.typing import ResponseReturnValue

from lightspark.lightspark_client import LightsparkSyncClient

app = Flask(__name__)

#################################################################
## MODIFY THOSE VARIABLES BEFORE RUNNING THE EXAMPLE
#################################################################
##
## We defined those variables as environment variables, but if you are just
## running the example locally, feel free to just set the values in Python.
##
## First, initialize your client ID and client secret. Those are available
## in your account at https://app.lightspark.com/api_config
##
## export LIGHTSPARK_API_TOKEN_CLIENT_ID=<client_id>
## export LIGHTSPARK_API_TOKEN_CLIENT_SECRET=<client_secret>
API_TOKEN_CLIENT_ID = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_ID")
API_TOKEN_CLIENT_SECRET = os.environ.get("LIGHTSPARK_API_TOKEN_CLIENT_SECRET")
##
## This example also assumes you already know your node UUID. Generally, an LNURL API would serve
## many different usernames while maintaining some internal mapping from username to node UUID. For
## simplicity, this example works with a single username and node UUID.
##
## export LIGHTSPARK_LNURL_NODE_UUID=0187c4d6-704b-f96b-0000-a2e8145bc1f9
LNURL_NODE_UUID = os.environ.get("LIGHTSPARK_LNURL_NODE_UUID")
LNURL_USERNAME = os.environ.get("LIGHTSPARK_LNURL_USERNAME", "ls_test")
##
## To run the webserver, run this command from the root of the SDK folder:
## $ pipenv run flask --app examples.flask_lnurl_server run
##
## By default the server will run on port 5000. You can make a request to the API through
## curl to make sure the server is working properly (replace ls_test with the username you have
## configured):
##
## $ curl http://127.0.0.1:7120/.well-known/lnurlp/ls_test
#################################################################

assert API_TOKEN_CLIENT_ID
assert API_TOKEN_CLIENT_SECRET
assert LNURL_NODE_UUID
assert LNURL_USERNAME


@dataclass
class User:
    uuid: UUID
    username: str
    node_uuid: str


LS_TEST_USER = User(
    # Static UUID so that callback URLs are always the same.
    UUID("4b41ae03-01b8-4974-8d26-26a35d28851b"),
    LNURL_USERNAME,
    f"LightsparkNode:{LNURL_NODE_UUID}",
)


def _generate_callback_for_user(user: User) -> str:
    return f"{request.url_root}api/lnurl/payreq/{user.uuid}"


def _generate_metadata_for_user(user: User) -> str:
    return json.dumps(
        [
            ["text/plain", f"Pay to domain.org user {user.username}"],
            ["text/identifier", f"{user.username}@domain.org"],
        ]
    )


@app.route("/.well-known/lnurlp/<username>")
def well_known_lnurlp_username(username: str) -> ResponseReturnValue:
    if username != LS_TEST_USER.username:
        abort(404, description=f"User not found: {username}")

    user = LS_TEST_USER
    callback = _generate_callback_for_user(user)
    metadata = _generate_metadata_for_user(user)

    return {
        "callback": callback,
        "maxSendable": 10_000_000,
        "minSendable": 1_000,
        "metadata": metadata,
        "tag": "payRequest",
    }


@app.route("/api/lnurl/payreq/<uuid>")
def lnurl_payreq(uuid: str) -> ResponseReturnValue:
    if uuid != str(LS_TEST_USER.uuid):
        abort(404, description=f"User not found: {uuid}")

    user = LS_TEST_USER
    amount_msats = int(request.args["amount"])

    ls_client = LightsparkSyncClient(
        api_token_client_id=API_TOKEN_CLIENT_ID,
        api_token_client_secret=API_TOKEN_CLIENT_SECRET,
    )

    invoice = ls_client.create_lnurl_invoice(
        user.node_uuid,
        amount_msats,
        _generate_metadata_for_user(user),
    )

    return {"pr": invoice.data.encoded_payment_request, "routes": []}


@app.errorhandler(404)
def error_not_found(e: Any) -> ResponseReturnValue:
    return {"status": "ERROR", "reason": e.description}, 404
