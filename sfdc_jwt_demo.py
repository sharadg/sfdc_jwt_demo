'''
Module to play around with sending JWT token info to Salesforce and receive an access token back
'''

from base64 import urlsafe_b64encode
from datetime import datetime, timedelta
import json
from urllib.parse import unquote
import requests
from flask import (
    Flask,
    render_template,
    jsonify,
)
import os
from cfenv import AppEnv
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

JWT_HEADER = '{"alg":"RS256"}'
JWT_CLAIM_ISS = "3MVG9ZF4bs_.MKuiyRq9J1l33OAR0jFoQbkx1am4Bzh5VDU1L5oSB500dxKTwobSPA7NuaVgl8VWwWV5tp_Vg"
JWT_CLAIM_SUB = "shgupta_dev@pivotal.io"
JWT_CLAIM_AUD = "https://login.salesforce.com"
JWT_AUTH_EP = "https://login.salesforce.com/services/oauth2/token"

app = Flask(__name__)


def jwt_claim():
    '''
    Function to package JWT Claim data in a base64 encoded string
    :return:
    base64 encoded jwt claims data
    '''

    claim_template = '{{"iss": "{0}", "sub": "{1}", "aud": "{2}", "exp": {3}}}'
    claim = urlsafe_b64encode(JWT_HEADER.encode()).decode()
    claim += "."

    # expiration_ts = (datetime.now(tz=timezone.utc) + timedelta(minutes=5)).timestamp()
    expiration_ts = int((datetime.now() + timedelta(seconds=300)).timestamp())
    payload = claim_template.format(JWT_CLAIM_ISS, JWT_CLAIM_SUB, JWT_CLAIM_AUD, expiration_ts)
    print(payload)

    claim += urlsafe_b64encode(payload.encode()).decode()
    return claim


def credhub_secret():
    cf_env = AppEnv()
    credhub_env = cf_env.get_service(label="credhub").get_url("demo-certificate")
    credhub_env = eval(unquote(credhub_env))

    return credhub_env


def get_private_key():
    credhub = credhub_secret()
    return credhub["value"]["private_key"]


def get_certificate():
    credhub = credhub_secret()
    return credhub["value"]["certificate"]


def sign_data(data):
    '''
    param: private_key_loc Path to your private key
    param: package Data to be signed
    return: base64 encoded signature
    '''
    key = get_private_key()
    rsakey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data.encode())
    sign = signer.sign(digest)

    # verify
    pubkey = rsakey.publickey()
    verifier = PKCS1_v1_5.new(pubkey)
    print("Verification: {}".format(verifier.verify(digest, sign)))

    return urlsafe_b64encode(sign).decode()


def do_auth(endpoint, data):
    '''
    Function to POST JWT claim to SFDC /oauth/token endpoint and receive an access_token
    :return:
    access token
    '''

    r = requests.post(endpoint, data=data)
    print(f"{r.headers!r}")
    print(f"{r.text!r}")
    return r


@app.route("/")
@app.route("/index")
def index():
    # Keeping with JWS spec, we need to remove the padding "=" characters from base64 encoded string
    claim = jwt_claim().replace("=", "")
    # print("JWT Claim: " + claim)

    # Keeping with JWS spec, we need to remove the padding "=" characters from base64 encoded string
    signed_claim = sign_data(claim).replace("=", "")
    # print("Signed JWT Claim: " + signed_claim)

    target_payload = claim + "." + signed_claim
    # print("Target payload: " + target_payload)

    auth_payload = {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": target_payload}
    response = do_auth(JWT_AUTH_EP, data=auth_payload)

    # return render_template("index.html", claim=claim, signed_claim=signed_claim, target_payload=target_payload, response=response)
    # return jsonify(claim=claim,
    #                 signed_claim=signed_claim,
    #                 target_payload=target_payload,
    #                 response_text=response.text,
    #                 response_headers=repr(response.headers))

    #  convert the text dictionary to data structure so it can be rendered as a json properly
    response_text = eval(response.text)
    response_headers = eval(str(response.headers))

    return_dict = {"claim": claim, "signed_claim": signed_claim, "target_payload": target_payload,
                   "response_text": response_text, "response_headers": response_headers}
    return jsonify(return_dict)


# @app.route("/info")
# def env_info():
#     dict_env = {k: v for k, v in os.environ.items()}
#     return jsonify(dict_env)


# @app.route("/debug")
# def debug_jsonify():
#     # dict = os.getenv("VCAP_SERVICES", "{}")
#     # dict = json.loads(dict)
#     # print(dict)
#
#     credhub_env = credhub_secret()
#     # credhub_env = json.loads(credhub_env)
#     # print(credhub_env)
#
#     return jsonify(credhub_env)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Run the app, listening on all IPs with our chosen port number
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=True)
