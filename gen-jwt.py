#!/usr/bin/env python

import hvac
import os
import shutil
from jwcrypto import jwk, jwt
from datetime import datetime

if os.path.isfile('./priv.pem'):
    shutil.copyfile('priv.pem', 'tmp.pem')
else:
    env_var = 'KEY_VER'

    # Need VAULT_ADDR and VAULT_TOKEN environment variables set
    client = hvac.Client()

    read_key_response = client.secrets.transit.read_key(name='jwt')

    if env_var in os.environ:
        keyVer = os.environ[env_var]
    else:
        keyVer = read_key_response['data']['latest_version']

    print("Key Version: %s" % keyVer)

    try:
        export_key_response = client.secrets.transit.export_key(
            name='jwt',
            key_type='signing-key',
            version=keyVer,
        )
    except hvac.exceptions.InvalidRequest:
        print('Key Version not allowed')
        exit(1)

    for k, v in export_key_response['data']['keys'].items():
        # print('Exported key: %s' % v)
        with open("tmp.pem", "w") as tmpfile:
            tmpfile.write(v)

with open("tmp.pem", "rb") as pemfile:
    privKey = jwk.JWK.from_pem(pemfile.read())

os.remove("tmp.pem")

now = datetime.now()
claimStr = "Token signed at: " + now.strftime("%d/%m/%Y %H:%M:%S")
Token = jwt.JWT(header={"alg": "RS256"},
                claims={"info": claimStr})
Token.make_signed_token(privKey)
print(Token.serialize())

with open("token.jwt", "w") as tokenfile:
    tokenfile.write(Token.serialize())
