#!/usr/bin/env python

import hvac
import os
from jwcrypto import jwk, jwt
from datetime import datetime

# Need VAULT_ADDR and VAULT_TOKEN environment variables set
client = hvac.Client()

export_key_response = client.secrets.transit.export_key(
    name='jwt',
    key_type='signing-key',
)

privKeyPEM = export_key_response['data']['keys']['1']
# print('Exported key: %s' % privKeyPEM)

with open("tmp.pem", "w") as tmpfile:
    tmpfile.write(privKeyPEM)

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
