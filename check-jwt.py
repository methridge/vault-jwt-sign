#!/usr/bin/env python

import hvac
import os
from jwcrypto import jwk, jwt

client = hvac.Client()

read_key_response = client.secrets.transit.read_key(name='jwt')
pubKeyPEM = read_key_response['data']['keys']['1']['public_key']
# print('Public KEY: {pem}'.format(pem=pubKeyPEM))

with open("tmp.pem", "w") as tmpfile:
    tmpfile.write(pubKeyPEM)

with open("tmp.pem", "rb") as pemfile:
    pubKey = jwk.JWK.from_pem(pemfile.read())

os.remove("tmp.pem")

with open("token.jwt", "r") as tokenfile:
    token = tokenfile.read()

ST = jwt.JWT(key=pubKey, jwt=token)
print(ST.claims)
