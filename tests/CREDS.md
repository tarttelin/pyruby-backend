# Creating dummy creds

Most of the values in the creds JSON file are not important. The private key though must be some valid PKCS#8 private key file.

To generate a fresh private key:
```bash
# Create a Private key
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:1024

## export the private key using nocrypt (Private key does have no password)
openssl pkcs8 -topk8 -in private.pem -nocrypt -out private_key.pem
```

The value of the `private_key` attribute in `dummy_creds.json` can now be replaced with the content of the new
`private_key.pem` file.