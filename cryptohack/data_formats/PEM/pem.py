from Crypto.PublicKey import RSA

with open("privacy_enhanced_mail.pem", "rb") as f:
    key = f.read()
key = RSA.import_key(key)

print("Private key: ", key.d)