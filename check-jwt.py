#!/usr/bin/env python

import hvac
import os
from jwcrypto import jwk, jwt, jws

with open("token.jwt", "r") as tokenfile:
    token = tokenfile.read()

# Need VAULT_ADDR and VAULT_TOKEN environment variables set
client = hvac.Client()

read_key_response = client.secrets.transit.read_key(name='jwt')

valid = False

for k, v in read_key_response['data']['keys'].items():
    pubKeyPEM = v['public_key']
    # print('Public KEY: {pem}'.format(pem=pubKeyPEM))

    with open("tmp.pem", "w") as tmpfile:
        tmpfile.write(pubKeyPEM)

    with open("tmp.pem", "rb") as pemfile:
        pubKey = jwk.JWK.from_pem(pemfile.read())

    os.remove("tmp.pem")

    try:
        ST = jwt.JWT(key=pubKey, jwt=token)
        print('Signed by key version: %s' % k)
        print(ST.claims)
        valid = True
        break
    except jws.InvalidJWSSignature:
        print('Not signed by key version: %s' % k)

if not valid:
    print('Token not signed by any key')
