# Signing a JWT with HashiCorp Vault Transit Secrets Engine - Advanced

## Transit Engine for Sign and Verify

To complete this example you need to have a Vault instance available and
unsealed. You will also need the following environment variables set.

```shell
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=x.abcdefghijk1234567
```

1. Enable transit engine

   ```shell
   vault secrets enable transit
   ```

1. Create our signing key

   ```shell
   vault write -f transit/keys/jwt type=rsa-4096 exportable=true
   ```

## Python Example

This python example uses the [HVAC](https://github.com/hvac/hvac/) client for
Vault and the [JWCrypto](https://github.com/latchset/jwcrypto/) libraries for
generating a JWT.

1. Install python dependancies

   ```shell
   pip install jwcrypto hvac
   ```

1. Generate token with `gen-jwt.py`

   ```shell
   ./gen-jwt.py
   ```

   This will output the JWT and write it to the file `token.jwt`

1. Verify token with `check-jwt.py`

   ```shell
   ./check-jwt.py
   ```

   This reads the token from the file (`token.jwt`) from the previous step and
   outputs the `info` claim.

   ```shell
   # Example
   $ ./check-jwt.py
   {"info":"Token signed at: 18/05/2021 15:36:22"}
   ```
